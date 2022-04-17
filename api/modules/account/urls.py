import os
from django.urls import path, include

app_name = os.getcwd().split(os.sep)[-1]

urlpatterns = (
    path("staff/", include("modules.account.staff.urls", namespace="staff")),
    path("role/", include("modules.account.role.urls", namespace="role")),
)
