from django.shortcuts import render

from .models import Profile


def index(request):
    result = Profile.objects.get_profile_links_timelines_for_superuser()
    context = dict(
        profile=result[0],
        links=result[1],
        timelines=result[2],
    )
    return render(request, "about/index.html", context)
