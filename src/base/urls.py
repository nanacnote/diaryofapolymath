import os

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path, reverse

urlpatterns = [
    path("admin/", admin.site.urls),
    path("about/", include(("about.urls", "about"), namespace="about")),
    path("blog/", include(("blog.urls", "blog"), namespace="blog")),
    path("exclusive/", include(("exclusive.urls", "exclusive"), namespace="exclusive")),
    path("", lambda _: redirect(reverse("blog:index"))),
]

if os.environ.get("APP_ENV") == "development":
    dev_urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns = urlpatterns + dev_urlpatterns
