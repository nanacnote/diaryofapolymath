from django.db.models import Count, F, Manager, Q


class PostManager(Manager):
    def get_post_by_slug(self, slug):
        return self.get(slug=slug)

    def get_published_posts(self):
        return self.filter(published=True).prefetch_related("tags")

    def get_tagged_posts(self, slug):
        return self.filter(Q(tags__slug=slug) & Q(published=True)).prefetch_related("tags")

    def get_archived_posts(self, slug):
        return self.filter(Q(published_on__year=slug) & Q(published=True)).prefetch_related("tags")

    def get_current_prev_next_posts(self, slug):
        current = self.prefetch_related("tags").get(slug=slug)
        previous = (
            self.filter(Q(published_on__lt=current.published_on) & Q(published=True))
            .order_by("-published_on")
            .first()
        )
        next = (
            self.filter(Q(published_on__gt=current.published_on) & Q(published=True))
            .order_by("published_on")
            .first()
        )
        return (current, previous, next)

    def group_posts_by_tag_with_count(self):
        return (
            self.filter(published=True)
            .annotate(name=F("tags__name"))
            .values("name")
            .annotate(count=Count("name"))
            .annotate(slug=F("tags__slug"))
            .order_by("name")
        )

    def group_posts_by_year_with_count(self):
        return (
            self.filter(published=True)
            .annotate(year=F("published_on__year"))
            .values("year")
            .annotate(count=Count("year"))
            .order_by("-year")
        )


class CommentManager(Manager):
    def get_comments_for_post(self, post_id):
        return self.filter(post_id=post_id, approved=True, deleted=False).order_by("created_on")

    def get_replies_for_comment(self, comment_id):
        return self.filter(parent_id=comment_id, approved=True, deleted=False).order_by(
            "created_on"
        )

    def get_comments_grouped_by_parent_for_post(self, post_id):
        comments = list(
            self.filter(post_id=post_id, approved=True, deleted=False)
            .select_related("parent")
            .order_by("created_on")
        )

        children_by_parent = {}
        for comment in comments:
            comment.children = []
            children_by_parent.setdefault(comment.parent_id, []).append(comment)

        for comment in comments:
            comment.children = children_by_parent.get(comment.id, [])

        return children_by_parent.get(None, [])
