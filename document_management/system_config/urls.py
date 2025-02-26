# system_config/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('user_info/', views.user_info, name='user_info'),
    path('change_password/', auth_views.PasswordChangeView.as_view(), name='change_password'),
    path('password_change_done/', views.password_change_done, name='password_change_done'),

]