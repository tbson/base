import os
from django.urls import path
from .views.auth import (
    LoginView,
    RefreshTokenView,
    RefreshCheckView,
    LogoutView,
    ResetPasswordView,
    ChangePasswordView,
)


app_name = os.getcwd().split(os.sep)[-1]
urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh-token/", RefreshTokenView.as_view(), name="refresh_token"),
    path("refresh-check/", RefreshCheckView.as_view(), name="refresh_check"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
]
