import logging

from django.shortcuts import render

logger = logging.getLogger(__name__)


def index(request):
    context = dict()
    return render(request, "etc/index.html", locals())
