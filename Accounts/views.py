from django.shortcuts import render
from .forms import SignupForm
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from .forms import LoginForm


# Create your views here.

class SignUpView(CreateView):
    form_class = SignupForm
    success_url='/'
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        messages.success(self.request,'Successfully Signed Up!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if form.errors:
            error_msg = str(form.errors.popitem()[1][0])
            messages.error(self.request,error_msg)
        return super().form_invalid(form)

class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form=LoginForm
    def form_valid(self, form):
        messages.success(self.request,'Successfully Signed In!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if form.errors:
            error_msg = str(form.errors.popitem()[1][0])
            messages.error(self.request,error_msg)
        return super().form_invalid(form)
    