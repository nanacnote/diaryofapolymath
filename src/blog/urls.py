from django.urls import path

from .views import feeds, views

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<slug:slug>/", views.post, name="post"),
    path("archive/<slug:slug>/", views.archive, name="archive"),
    path("tag/<slug:slug>/", views.tag, name="tag"),
    path("feed/rss.xml", feeds.RssLatestPostsFeed(), name="rss"),
    path("feed/atom.xml", feeds.AtomLatestPostsFeed(), name="atom"),
]
