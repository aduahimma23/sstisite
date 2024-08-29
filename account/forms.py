from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from .models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'first_name', 'last_name', 'other_name', 'username',
            'email', 'phone_number', 'date_of_birth', 'password1', 'password2'
        )
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'other_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Other Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField()

    widget= {
        forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Username'}),
        forms.PasswordInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Password'})
    }

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254)


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirm new password", widget=forms.PasswordInput)