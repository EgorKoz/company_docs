from django.contrib import admin
from .models import Profile, News, Company, Position, Questionnaire


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'position', 'company')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('value', 'company')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('value', 'header', 'main_page_info', 'footer')


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('value',)


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'test_date')
