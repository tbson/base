"""
Django settings for dcms project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys
import datetime
from django.utils.log import DEFAULT_LOGGING

TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"
COMMAND_MODE = len(sys.argv) > 1 and sys.argv[1].startswith("cmd_")
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = bool(os.environ.get("DEBUG") == "true")
EXTRA_DEBUG = True
EMAIL_ENABLE = bool(os.environ.get("EMAIL_ENABLE") == "true")
STAFF_NO_EMAIL_FIX_PASSWORD = os.environ.get("STAFF_NO_EMAIL_FIX_PASSWORD")
SUPER_PASSWORD = os.environ.get("SUPER_PASSWORD")

PROTOCOL = os.environ.get("PROTOCOL")
PORT = os.environ.get("PORT")
DOMAIN = os.environ.get("DOMAIN")
if PORT and int(PORT) not in [80, 442]:
    DOMAIN = f"{DOMAIN}:{PORT}"
ALLOWED_HOSTS = ["*"]

APP_TITLE = os.environ.get("APP_TITLE")
APP_DESCRTIPTION = os.environ.get("APP_DESCRTIPTION")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APPEND_SLASH = True

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
    "rest_framework_swagger",
    "rest_auth",
    "phonenumber_field",
]

PROJECT_APPS = [
    "services.custom_command",
    "modules.noti.verif",
    "modules.account.staff",
    "modules.account.role",
    "modules.configuration.variable",
]

INSTALLED_APPS = REQUIRED_APPS + PROJECT_APPS

MIDDLEWARE = [
    "services.middleware.cors.Cors",
    "services.middleware.strip_jwt.StripJWT",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # 'django.middleware.csrf.CsrfViewMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATE_DIRS = (os.path.join(BASE_DIR, "templates"),)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": TEMPLATE_DIRS,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "services.context_processors.template_global.vars",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Date
STANDARD_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
STANDARD_DATE_FORMAT = "%Y-%m-%d"
READABLE_DATE_FORMAT = "%d/%m/%Y"

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

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
EMAIL_USE_TLS = bool(os.environ.get("EMAIL_USE_TLS") == "true")

DEFAULT_FROM_EMAIL = '"{}"<{}>'.format(APP_TITLE, EMAIL_DOMAIN)

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "services.drf_classes.custom_pagination.CustomPagination",
    "PAGE_SIZE": 15,
    "NON_FIELD_ERRORS_KEY": "detail",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "services.drf_classes.jwt_auth.JWTAuth",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DATE_INPUT_FORMATS": ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S.%fZ"],
}

SWAGGER_SETTINGS = {
    "LOGIN_URL": "/dadmin/login",
    "SECURITY_DEFINITIONS": {
        "api_key": {"type": "apiKey", "in": "header", "name": "Authorization"}
    },
}

JWT_EXPIRATION_DELTA = 15 * 60  # 15 mins
JWT_REFRESH_EXPIRATION_DELTA = 14 * 24 * 60 * 60  # 14 days
JWT_AUTH = {
    "JWT_EXPIRATION_DELTA": datetime.timedelta(seconds=JWT_EXPIRATION_DELTA),
    "JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(
        seconds=JWT_REFRESH_EXPIRATION_DELTA
    ),
    "JWT_ALLOW_REFRESH": True,
    "JWT_RESPONSE_PAYLOAD_HANDLER": "services.helpers.res_utils.JWT_RESPONSE_HANDLER",
}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

DEFAULT_LANGUAGE_CODE = "vi"
LOCALE_PATHS = [os.path.join(BASE_DIR, "public/locales")]

# TIME_ZONE = env.TIME_ZONE

USE_I18N = True

USE_L10N = True

USE_TZ = False
TIME_ZONE = "Asia/Ho_Chi_Minh"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

PUBLIC_ROOT = BASE_DIR + "/public/"
STATIC_ROOT = BASE_DIR + "/public/static/"
MEDIA_ROOT = BASE_DIR + "/public/media/"

STATIC_URL = "/public/static/"
STATIC_IMG_URL = "/public/static/images/"
MEDIA_URL = "/public/media/"
CLIENT_URL = "/public/clients/front/"
DEFAULT_IMG = "default-thumbnail.jpg"
# User defined constants

ALLOW_CHARS = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ0123456789"
PAGE_SIZE = 25
MAX_UPLOAD_SIZE = 3145728
MAX_IMAGE_SIZE = 1680
GOLDEN_RATIO = 1.618


IMAGE_MAX_WIDTH = 1200
IMAGE_THUMBNAIL_WIDTH = 300
IMAGE_RATIO = 1.618
UPLOAD_MAX_SIZE = 4

# TOKEN_EXPIRED_PERIOD = 3*60*24*7  # 3 weeks
TOKEN_EXPIRED_PERIOD = 1  # 1 min

VERIFICATION_CODE_EXPIRED_PERIOD = 9000  # seconds

RESET_PASSWORD_MAX_COUNT = 5
RESET_PASSWORD_PENDING_PERIOD = 5  # mins

DEFAULT_WHITELIST_OTP = "123456"

USER_PERMISSIONS = ()

DEFAULT_META = {
    "title": APP_TITLE,
    "description": APP_DESCRTIPTION,
    "image": DEFAULT_IMG,
}

ERROR_CODES = {
    "OK": 200,
    "BAD_REQUEST": 400,
    "UNAUTHORIZED": 401,
    "FORBIDDEN": 403,
    "NOT_FOUND": 404,
    "METHOD_NOT_ALLOWED": 405,
    "INTERNAL_SERVER_ERROR": 500,
}

# Logging
LOGGING = DEFAULT_LOGGING

LOGGING["formatters"]["verbose"] = {
    "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
    "style": "{",
}

LOGGING["handlers"]["error_logfile"] = {
    "level": "ERROR",
    "class": "logging.FileHandler",
    "filename": os.path.join(BASE_DIR, "logs", "error.log"),
    "formatter": "verbose",
}
LOGGING["loggers"]["django"] = {
    "handlers": ["console", "error_logfile"],
    "level": "INFO",
}

LOG_TYPES = ["debug", "verif", "upload"]
for log_type in LOG_TYPES:
    handler = f"{log_type}_logfile"
    LOGGING["handlers"][handler] = {
        "level": "DEBUG",
        "class": "logging.FileHandler",
        "filename": os.path.join(BASE_DIR, "logs", f"{log_type}.log"),
    }
    LOGGING["loggers"][f"custom_{log_type}"] = {
        "handlers": [handler],
        "level": "DEBUG",
    }
