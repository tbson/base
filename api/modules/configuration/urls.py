import os
from django.urls import path, include

app_name = os.getcwd().split(os.sep)[-1]

urlpatterns = (
    path(
        "variable/",
        include("modules.configuration.variable.urls", namespace="variable"),
    ),
)
