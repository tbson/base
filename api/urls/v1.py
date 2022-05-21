import os
from django.urls import path, include

app_name = os.getcwd().split(os.sep)[-1]

urlpatterns = (
    path("noti/", include("modules.noti.urls", namespace="noti")),
    path("account/", include("modules.account.urls", namespace="account")),
    path(
        "configuration/",
        include("modules.configuration.urls", namespace="configuration"),
    ),
)
