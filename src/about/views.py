from django.shortcuts import render

from .models import Link, Profile, Timeline


def index(request):
    profile = Profile.objects.get(is_superuser=True)
    context = dict(
        profile=profile,
        links=profile.link_set.all(),
        timelines=profile.timeline_set.all(),
    )
    return render(request, "about/index.html", context)
