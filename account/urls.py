from django.urls import path

from .views import (RegistrationView, ActivationView, LoginView, LogoutView,
                    ForgotPasswordView, ChangePasswordView)

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='register-account'),
    path('activate/', ActivationView.as_view(), name='acc-activation'),
    path('login/', LoginView.as_view(), name='login-page'),
    path('logout/', LogoutView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
]
