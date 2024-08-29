from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import *


def signup_view(request):
    if request.method == 'POST':
        forms = CustomUserCreationForm(request.POST)
        try:
            if forms.is_valid():
                user = forms.save(commit=False)
                auth_login(request, user)
                messages.success(request, 'Signup Sucessufully')
                return redirect('home')
        except ValueError as err:
            messages.error(request, f'Check the details provided {err}')
    else:
         forms = CustomUserCreationForm()

    return render(request, 'account/signup.html', {'form': forms})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Login successful')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = AuthenticationForm()

    return render(request, 'account/login.html', {'form': form})

def logout(request):
    auth_login(request)
    return redirect('login')
