"""
Django settings
"""
import os
from corsheaders.defaults import default_headers
import getconf

CONFIG = getconf.ConfigGetter("mds")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = CONFIG.getstr(
    "django.secret_key", "weak", doc="Secret key for signing data"
)
DEBUG = CONFIG.getbool("dev.debug", False)

ALLOWED_HOSTS = CONFIG.getlist(
    "django.allowed_hosts", [], doc="Comma-separated list of allowed hosts"
)

INSTALLED_APPS = [
    "mds.apps.Config",
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "rest_framework",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]
ROOT_URLCONF = "mds.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]
WSGI_APPLICATION = "mds.server.wsgi.application"
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": CONFIG.getstr("db.name", "mds"),
        "USER": CONFIG.getstr("db.user", "postgres"),
        "PASSWORD": CONFIG.getstr("db.password"),
        "HOST": CONFIG.getstr("db.host", "127.0.0.1"),
        "PORT": CONFIG.getstr("db.port", "5432"),
        "ATOMIC_REQUESTS": True,
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"}
]
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = "/static/"
LOCALE_PATH = (os.path.join(BASE_DIR, "locale"),)

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers) + ["cache-control"]

REST_FRAMEWORK = {
    # "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "mds.access_control.authentication.StatelessJwtAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    )
}

JWT_AUTH = {
    # Space separated secret keys
    "JWT_SECRET_KEYS": CONFIG.getstr("jwt.secret_keys", None),
    # Concatenated pem public keys (-----BEGIN PUBLIC KEY-----)
    "JWT_PUBLIC_KEYS": CONFIG.getstr("jwt.public_keys", None),
}
if not JWT_AUTH["JWT_SECRET_KEYS"] and not JWT_AUTH["JWT_PUBLIC_KEYS"]:
    raise Exception(
        "JWT authentication configuration is incomplete: neither secret nor public key found"
    )
