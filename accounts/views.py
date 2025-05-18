from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash

from accounts.models import User
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('change-password')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Pour éviter la déconnexion
            request.user.first_login = False
            request.user.save()
            return redirect('dashboard')  # à adapter selon ta suite
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def account_settings_view(request):
    user = request.user
    form = CustomUserCreationForm(instance=user)
    password_form = PasswordChangeForm(user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            form = CustomUserCreationForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profil mis à jour.")
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, "Mot de passe mis à jour.")

    return render(request, 'accounts/settings.html', {
        'form': form,
        'password_form': password_form
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # ou toute autre page par défaut
        else:
            messages.error(request, "Identifiants invalides.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})



class AvatarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']

@login_required
def account_settings_view(request):
    user = request.user
    avatar_form = AvatarForm(instance=user)
    password_form = PasswordChangeForm(user)

    if request.method == 'POST':
        if 'update_avatar' in request.POST:
            avatar_form = AvatarForm(request.POST, request.FILES, instance=user)
            if avatar_form.is_valid():
                avatar_form.save()
                messages.success(request, "Avatar mis à jour.")
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, "Mot de passe mis à jour.")
                return redirect('account-settings')

    return render(request, 'accounts/settings.html', {
        'avatar_form': avatar_form,
        'password_form': password_form
    })
