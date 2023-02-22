from collections import Counter
from operator import itemgetter

from django.shortcuts import render

from .models import Post, Tag


def index(request):
    posts = Post.objects.all()
    archives = Counter()
    for post in posts:
        archives[post.published_on.year] += 1
    payload = dict(
        posts=posts,
        archives=sorted(archives.items(), key=itemgetter(0)),
        tags=Tag.objects.all(),
    )
    return render(request, "blog/index.html", payload)


def post(request, slug):
    posts = Post.objects.all()
    archives = Counter()
    for post in posts:
        archives[post.published_on.year] += 1
    payload = dict(
        post=posts.get(slug=slug),
        archives=sorted(archives.items(), key=itemgetter(0)),
        tags=Tag.objects.all(),
    )
    return render(request, "blog/post.html", payload)


def archive(request, slug):
    posts = Post.objects.all()
    archives = Counter()
    for post in posts:
        archives[post.published_on.year] += 1
    payload = dict(
        posts=posts.filter(published_on__year=slug),
        archives=sorted(archives.items(), key=itemgetter(0)),
        tags=Tag.objects.all(),
    )
    return render(request, "blog/archive.html", payload)


def tag(request, slug):
    posts = Post.objects.all()
    archives = Counter()
    for post in posts:
        archives[post.published_on.year] += 1
    payload = dict(
        posts=posts.filter(
            tags__name__istartswith=slug.split("-")[0],
            tags__name__iendswith=slug.split("-")[-1],
        ),
        archives=sorted(archives.items(), key=itemgetter(0)),
        tags=Tag.objects.all(),
    )
    return render(request, "blog/tag.html", payload)
