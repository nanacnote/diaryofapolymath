from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<slug:slug>/", views.post, name="post"),
    path("archive/<slug:slug>/", views.archive, name="archive"),
    path("tag/<slug:slug>/", views.tag, name="tag"),
]
