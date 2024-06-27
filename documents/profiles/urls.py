from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/', views.settings_view, name='settings'),
    path('settings/profile', views.profile_handler, name='profile_create'),
    path('settings/news', views.news_handler, name='news_create'),
    path('settings/position', views.position_handler, name='position_create'),
    path('quest/', views.QuestionnaireView.as_view(), name='questionnaire'),
    path('delete/<int:pk>', views.delete_questionnaire, name='delete'),
    path('', views.main_view, name='main_view'),
]
