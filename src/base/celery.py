import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings.production")

app = Celery("scheduler")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"
app.autodiscover_tasks()
