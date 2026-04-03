import os

from base.settings.base import *

DEBUG = False
STATIC_ROOT = "/var/www/"
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = [os.environ.get("DJANGO_DOMAIN_NAME")]

PROD_APPS = []

INSTALLED_APPS = INSTALLED_APPS + PROD_APPS

PROD_MIDDLEWARE = [
    "base.middlewares.GoatcounterAnalyticsMiddleware",
]

MIDDLEWARE = MIDDLEWARE + PROD_MIDDLEWARE

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DJANGO_DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST"),
        "PORT": os.environ.get("DATABASE_PORT"),
    }
}

CELERY_TASK_ALWAYS_EAGER = False
