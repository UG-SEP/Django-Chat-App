from django.urls import path
from django.contrib.auth import views as auth_views
from Accounts.forms import UserPasswordResetForm,UserPasswordResetConfirmForm,UserPasswordChangeForm
from .views import UserLoginView,SignUpView


urlpatterns = [
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('signup/',SignUpView.as_view(),name='signup'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html',form_class=UserPasswordResetForm),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html',form_class=UserPasswordResetConfirmForm),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/security.html',form_class=UserPasswordChangeForm,success_url='/'), name='password_change'),
]