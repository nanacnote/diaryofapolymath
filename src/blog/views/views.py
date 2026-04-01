import logging

from django.shortcuts import redirect, render
from django.urls import reverse

from base.integrations.matrix.notifier import notify_new_comment

from ..forms import CommentForm
from ..models import Comment, Post

logger = logging.getLogger(__name__)


# TODO: gracefully handle slug not found (404) and other errors (500)
def index(request):
    posts = Post.objects.get_published_posts()
    tags = Post.objects.group_posts_by_tag_with_count()
    archives = Post.objects.group_posts_by_year_with_count()
    return render(request, "blog/index.html", locals())


def post(request, slug):
    comment_form = CommentForm()

    if request.method == "POST" and not (comment_form := postCommentPOST(request, slug)):
        return redirect(f"{reverse('blog:post', kwargs={'slug': slug})}?submitted=1")

    (post, prev, next) = Post.objects.get_current_prev_next_posts(slug)
    tags = Post.objects.group_posts_by_tag_with_count()
    archives = Post.objects.group_posts_by_year_with_count()
    comments = Comment.objects.get_comments_grouped_by_parent_for_post(post.id)
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


# ---------
# POST HANDLERS
# ---------
def postCommentPOST(request, slug):
    comment_form = CommentForm(request.POST)
    if not comment_form.is_valid():
        return comment_form

    comment = comment_form.save(commit=False)
    comment.post = Post.objects.get_post_by_slug(slug)
    comment.save()

    notify_new_comment(comment)
