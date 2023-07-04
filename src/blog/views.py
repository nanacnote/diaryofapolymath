from django.shortcuts import render

from .models import Post


def index(request):
    posts = Post.objects.get_published_posts()
    tags = Post.objects.group_posts_by_tag_with_count()
    archives = Post.objects.group_posts_by_year_with_count()
    return render(request, "blog/index.html", locals())


def post(request, slug):
    (post, prev, next) = Post.objects.get_current_prev_next_posts(slug)
    tags = Post.objects.group_posts_by_tag_with_count()
    archives = Post.objects.group_posts_by_year_with_count()
    return render(request, "blog/post.html", locals())


def archive(request, slug):
    posts = Post.objects.get_archived_posts(slug)
    archives = Post.objects.group_posts_by_year_with_count()
    tags = Post.objects.group_posts_by_tag_with_count()
    return render(request, "blog/archive.html", locals())


def tag(request, slug):
    posts = Post.objects.get_tagged_posts(slug)
    archives = Post.objects.group_posts_by_year_with_count()
    tags = Post.objects.group_posts_by_tag_with_count()
    return render(request, "blog/tag.html", locals())
