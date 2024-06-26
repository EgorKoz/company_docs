from functools import cache

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Company


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if not user:
            messages.success(request, 'Try again')

            return redirect('login')

        login(request, user)
        request.session['company'] = (
            Profile.objects.get(user__username=request.user).company_id)
        messages.success(request, 'Login successful')

        return redirect('main_view')
    else:
        return render(request, 'login.html', {})


@cache
def get_company_info(company_id):
    return Company.objects.get(id=company_id)


@login_required()
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful')

    return redirect('login')


@login_required()
def main_view(request):
    company = get_company_info(request.session['company'])
    return render(
        request, 'main_page.html', {'company': company})


