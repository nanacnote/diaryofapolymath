from django import template
from readtime import of_text

register = template.Library()


@register.filter
def read_time(content):
    return of_text(content)
