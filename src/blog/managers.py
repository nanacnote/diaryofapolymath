from django.db.models import Count, F, Manager, Q


class PostManager(Manager):
    def get_published_posts(self):
        return self.filter(published=True).prefetch_related("tags")

    def get_tagged_posts(self, slug):
        return self.filter(Q(tags__slug=slug) & Q(published=True)).prefetch_related(
            "tags"
        )

    def get_archived_posts(self, slug):
        return self.filter(
            Q(published_on__year=slug) & Q(published=True)
        ).prefetch_related("tags")

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
