import os
from django.urls import path
from .views.auth import (
    ProfileView,
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
    path("profile/", ProfileView.as_view(), name="profile"),
]
