# system_config/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect


@login_required
def user_info(request):
    user = request.user
    return render(request, 'system_config/user_info.html', {'user': user})


def password_change_done(request):

    return redirect('home')


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'system_config/change_password.html'
    success_url = reverse_lazy('home')