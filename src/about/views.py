import logging

from django.shortcuts import render

from .models import Profile

logger = logging.getLogger(__name__)


def index(request):
    profile, links, timelines = Profile.objects.get_profile_links_timelines_for_superuser()
    return render(request, "about/index.html", locals())
