from django import forms
from django.contrib.auth.models import User
from .models import Questionnaire, Profile, News, Position
from .utils import generate_word


class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        exclude = ('user', 'file')
        labels = {
            "fio": ("Ф.И.О. работника"),
            "post": ("Должность"),
            "test_date": ("Дата проверки знаний"),
            "company_name": ("Наименование компании"),
            "chairman": ("ФИО Председателя комиссии"),
            "chairman_post": ("Должность председателя комиссии"),
            "first_man": ("ФИО 1-го члена комиссии"),
            "first_man_post": ("Должность 1-го члена комиссии"),
            "second_man": ("ФИО 2-го члена комиссии"),
            "second_man_post": ("Должность 2-го члена комиссии"),
            "responsible_electrical": ("Ответственный за электрохозяйство"),
            "reason_check": ("Причина проверки знаний"),
            "fire_check": ("Противопожарный инструктаж"),
            "post_code": ("№ программы"),
            "group": ("группа ЭБ"),
            "experience": ("Стаж работы"),
            "certificate": ("Номер удостоверения по специальности")
        }
        help_texts = {
            "test_date": "YYYY-MM-DD",
        }

    def generate_file_name(self):
        from datetime import datetime
        directory = self.instance.user
        date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        return f'{directory}/{date}.pdf'

    def convert_data(self):
        date = self.cleaned_data['test_date']
        self.cleaned_data['test_date'] = date.strftime('%d.%m.%Y')

    def convert_choice(self):
        for item in ('reason_check', 'group', 'fire_check'):
            data = self.cleaned_data[item]
            self.cleaned_data[item] = dict(self.fields[item].choices)[data]

    def make_docs_template(self):
        file = self.generate_file_name()
        self.convert_choice()
        self.convert_data()
        self.cleaned_data['id'] = self.instance.id
        try:
            generate_word(file, self.cleaned_data)
        except Exception as e:
            print(e)
            file = None

        return file


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'company')


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password')


class NewsCreateForm(forms.ModelForm):
    class Meta:
        model = News
        exclude = ('created_at', 'company')


class PositionCreateForm(forms.ModelForm):
    class Meta:
        model = Position
        exclude = ()
