from django.shortcuts import render

from .models import Link, Profile, Timeline


def index(request):
    payload = dict(
        profile=Profile.objects.all().first(),
        links=Link.objects.all(),
        timelines=Timeline.objects.all(),
    )
    return render(request, "about/index.html", payload)
