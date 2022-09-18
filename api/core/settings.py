"""
Django settings for sampledjango project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""


import os
import sys
from pathlib import Path
from datetime import timedelta
from django.utils.log import DEFAULT_LOGGING

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG") == "true"

ALLOWED_HOSTS = ["*"]


# Application definition
REQUIRED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_auth",
    "phonenumber_field",
]

PROJECT_APPS = [
    "module.custom_cmd",
    "module.noti.verif",
    "module.account.user",
    "module.account.staff",
    "module.account.role",
    "module.conf.variable",
]

INSTALLED_APPS = REQUIRED_APPS + PROJECT_APPS

MIDDLEWARE = [
    "service.framework.middleware.strip_jwt.StripJWT",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
        "TEST": {
            "NAME": os.environ.get("DB_TEST"),
        },
    },
}

# Email

EMAIL_DOMAIN = os.environ.get("EMAIL_DOMAIN")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 0))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS") == "true"

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "vi-vn"

TIME_ZONE = "Asia/Ho_Chi_Minh"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "/public/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

APPEND_SLASH = True

AUTH_USER_MODEL = "user.User"

# Logging
LOGGING = DEFAULT_LOGGING

LOGGING["formatters"]["verbose"] = {
    "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
    "style": "{",
}

LOGGING["handlers"]["error_logfile"] = {
    "level": "ERROR",
    "class": "logging.FileHandler",
    "filename": os.path.join(BASE_DIR, "log", "error.log"),
    "formatter": "verbose",
}
LOGGING["loggers"]["django"] = {
    "handlers": ["console", "error_logfile"],
    "level": "INFO",
}

LOG_TYPES = ["debug", "verif"]
for log_type in LOG_TYPES:
    handler = f"{log_type}_logfile"
    LOGGING["handlers"][handler] = {
        "level": "DEBUG",
        "class": "logging.FileHandler",
        "filename": os.path.join(BASE_DIR, "log", f"{log_type}.log"),
    }
    LOGGING["loggers"][f"custom_{log_type}"] = {
        "handlers": [handler],
        "level": "DEBUG",
    }

##################################################
# Custom settings                                #
##################################################

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "UPDATE_LAST_LOGIN": True,
}

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "service.framework.drf_class.custom_pagination.CustomPagination",
    "PAGE_SIZE": 15,
    "NON_FIELD_ERRORS_KEY": "detail",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DATE_INPUT_FORMATS": ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S.%fZ"],
}

TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"
COMMAND_MODE = len(sys.argv) > 1 and sys.argv[1].startswith("cmd_")
EMAIL_ENABLE = os.environ.get("EMAIL_ENABLE") == "true"

PROTOCOL = os.environ.get("PROTOCOL")
PORT = os.environ.get("PORT")
DOMAIN = os.environ.get("DOMAIN")
if PORT and int(PORT) not in [80, 442]:
    DOMAIN = f"{DOMAIN}:{PORT}"
CSRF_TRUSTED_ORIGINS = [f"{PROTOCOL}://{DOMAIN}"]

APP_TITLE = os.environ.get("APP_TITLE")
APP_DESCRTIPTION = os.environ.get("APP_DESCRTIPTION")
DEFAULT_FROM_EMAIL = f'"{APP_TITLE}"<{EMAIL_DOMAIN}>'

VERIFICATION_CODE_EXPIRED_PERIOD = 120  # seconds

# Date
STANDARD_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
STANDARD_DATE_FORMAT = "%Y-%m-%d"
READABLE_DATE_FORMAT = "%d/%m/%Y"

LOCALE_PATHS = [os.path.join(BASE_DIR, "public/locales")]

PUBLIC_ROOT = os.path.join(BASE_DIR, "public")
STATIC_ROOT = os.path.join(BASE_DIR, "public", "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "public", "media")

STATIC_IMG_URL = "/public/static/images/"
MEDIA_URL = "/public/media/"
CLIENT_URL = "/public/clients/front/"

# Image configs
IMAGE_MAX_WIDTH = 1200
