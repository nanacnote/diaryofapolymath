import os

from .base import *

DEBUG = False
STATIC_ROOT = "/var/www/"
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = [os.environ.get("NGINX_SERVER_NAME")]
