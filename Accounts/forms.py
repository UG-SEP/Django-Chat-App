from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,SetPasswordForm,PasswordResetForm,PasswordChangeForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),label_suffix='')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control','placeholder': 'Enter your password'}),label_suffix='')


class SignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),label_suffix='')
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control','placeholder': 'Enter your password'}),label_suffix='',label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control','placeholder': 'Enter your password'}),label_suffix='',label='Confirm Password')


class UserPasswordResetForm(PasswordResetForm):

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'placeholder': 'Email Address',
        'class': 'form-control',
        'id' : 'email'
        }),label_suffix='')


class UserPasswordResetConfirmForm(SetPasswordForm):

    new_password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter New Password',
        'class': 'form-control'
        }))
    new_password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm New Password',
        'class': 'form-control'
        }))


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your old Password',
        'id': 'currentPassword',
        'class':'form-control',
    }),label_suffix='',label='Old Password')

    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your new Password',
        'id': 'newPassword',
        'class':'form-control',
    }),label_suffix='',label='New Password')

    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'id': 'confirmPassword',
        'class':'form-control',
    }),label_suffix='',label='Confirm Password')

