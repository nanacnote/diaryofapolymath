from django.shortcuts import render

from .models import Profile


def index(request):
    (
        profile,
        links,
        timelines,
    ) = Profile.objects.get_profile_links_timelines_for_superuser()
    return render(request, "about/index.html", locals())
