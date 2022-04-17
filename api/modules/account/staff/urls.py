import os
from django.urls import path
from .views.auth import (
    LoginView,
    RefreshView,
    RefreshCheckView,
    LogoutView,
    SignupView,
    ProfileView,
    ResetPasswordView,
    ChangePasswordView,
)
from .views.crud import StaffViewSet

BASE_ENDPOINT = StaffViewSet.as_view(
    {"get": "list", "post": "add", "delete": "delete_list"}
)

PK_ENDPOINT = StaffViewSet.as_view(
    {"get": "retrieve", "put": "change", "delete": "delete"}
)


app_name = os.getcwd().split(os.sep)[-1]
urlpatterns = [
    path("", BASE_ENDPOINT),
    path("<int:pk>", PK_ENDPOINT),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="refresh"),
    path("refresh-check/", RefreshCheckView.as_view(), name="refresh-check"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("reset-password/", ResetPasswordView.as_view(), name="resetPassword"),
    path("change-password/", ChangePasswordView.as_view(), name="changePassword"),
]
