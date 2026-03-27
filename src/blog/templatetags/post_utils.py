import timeago
from django import template
from django.utils import timezone
from readtime import of_text

register = template.Library()


@register.filter
def read_time(content):
    return of_text(content)


@register.filter
def time_ago(since):
    return timeago.format(since, timezone.now())


@register.filter
def email_to_name(value):
    return str(value).split("@", 1)[0].replace(".", " ").replace("_", " ").title()
