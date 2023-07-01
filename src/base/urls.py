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
