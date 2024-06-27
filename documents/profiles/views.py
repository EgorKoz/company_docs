from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User

from .models import Questionnaire
from .forms import (
    QuestionnaireForm, ProfileCreateForm, UserCreateForm, NewsCreateForm,
    PositionCreateForm)


def redirect_not_admin_user(view, redirect_to='main_view'):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.user.profile.is_admin:
            return view(request, *args, **kwargs)
        else:
            return redirect(redirect_to)
    return wrapper


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if not user:
            messages.success(request, 'Try again')

            return redirect('login')

        login(request, user)
        messages.success(request, 'Login successful')

        return redirect('main_view')
    else:
        return render(request, 'login.html', {})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful')

    return redirect('login')


@login_required
def main_view(request):
    return render(request, 'main_page.html', {})


class QuestionnaireView(CreateView):
    form_class = QuestionnaireForm
    template_name = 'questionnaire.html'
    success_url = reverse_lazy('questionnaire')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(QuestionnaireView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['docs'] = self.request.user.questionnaire_set.all()
        return context

    def get_initial(self):
        user: User = self.request.user
        return {
            'company_name': user.profile.company,
            'fio': f'{user.last_name} {user.first_name}',
            'post': user.profile.position
        }

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        file = form.make_docs_template()
        if not file:
            messages.success(self.request, 'Error. Try one.')

            return redirect('questionnaire')
        instance.file = file
        instance.save()
        return super().form_valid(form)


@login_required
def delete_questionnaire(request, pk):
    doc = get_object_or_404(Questionnaire, pk=pk)
    doc.delete()

    return redirect('questionnaire')


@login_required
@redirect_not_admin_user
def settings_view(request):
    user_form = UserCreateForm(prefix='user')
    profile_form = ProfileCreateForm(prefix='profile')
    news_form = NewsCreateForm(prefix='news')
    position_form = PositionCreateForm(prefix='position')

    return render(
        request,
        'settings.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
            'news_form': news_form,
            'position_form': position_form
        }
    )


@login_required
@redirect_not_admin_user
def profile_handler(request):
    if request.method == 'POST':
        user_form = UserCreateForm(request.POST, prefix='user')
        profile_form = ProfileCreateForm(request.POST, prefix='profile')
        if all([user_form.is_valid(), profile_form.is_valid()]):
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.company = request.user.profile.company
            profile.save()

    return redirect('settings')


@login_required
@redirect_not_admin_user
def news_handler(request):
    if request.method == 'POST':
        form = NewsCreateForm(request.POST, prefix='news')
        if form.is_valid():
            form = form.save(commit=False)
            form.company = request.user.profile.company
            form.save()

    return redirect('settings')


@login_required
@redirect_not_admin_user
def position_handler(request):
    if request.method == 'POST':
        form = PositionCreateForm(request.POST, prefix='position')
        if form.is_valid():
            form.save()

    return redirect('settings')
