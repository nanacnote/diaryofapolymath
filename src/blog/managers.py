from django.db.models import Count, F, Func, Manager, Value
from django.db.models.functions import Lower


class PostManager(Manager):
    def get_current_previous_next_post_by_slug(self, slug):
        current = self.get(slug=slug)
        previous = (
            self.filter(published_on__lt=current.published_on)
            .order_by("-published_on")
            .first()
        )
        next = (
            self.filter(published_on__gt=current.published_on)
            .order_by("published_on")
            .first()
        )

        return (current, previous, next)

    def group_posts_by_tag_with_count(self):
        return (
            self.annotate(name=F("tags__name"))
            .values("name")
            .annotate(count=Count("name"))
            .annotate(slug=F("tags__slug"))
            .order_by("name")
        )

    def group_posts_by_year_with_count(self):
        return (
            self.annotate(year=F("published_on__year"))
            .values("year")
            .annotate(count=Count("year"))
            .order_by("-year")
        )
