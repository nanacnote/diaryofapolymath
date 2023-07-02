from django.shortcuts import render

from .models import Post


def index(request):
    context = dict(
        posts=Post.objects.get_published_posts(),
        tags=Post.objects.group_posts_by_tag_with_count(),
        archives=Post.objects.group_posts_by_year_with_count(),
    )
    return render(request, "blog/index.html", context)


def post(request, slug):
    (post, prev, next) = Post.objects.get_current_previous_next_posts_by_slug(slug=slug)
    context = dict(
        post=post,
        prev=prev,
        next=next,
        tags=Post.objects.group_posts_by_tag_with_count(),
        archives=Post.objects.group_posts_by_year_with_count(),
    )
    return render(request, "blog/post.html", context)


def archive(request, slug):
    context = dict(
        posts=Post.objects.get_archived_posts_by_slug(slug),
        archives=Post.objects.group_posts_by_year_with_count(),
        tags=Post.objects.group_posts_by_tag_with_count(),
    )
    return render(request, "blog/archive.html", context)


def tag(request, slug):
    context = dict(
        posts=Post.objects.get_tagged_posts_by_slug(slug),
        archives=Post.objects.group_posts_by_year_with_count(),
        tags=Post.objects.group_posts_by_tag_with_count(),
    )
    return render(request, "blog/tag.html", context)
