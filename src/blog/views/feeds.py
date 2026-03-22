from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed as AtomFeed
from django.utils.feedgenerator import Rss201rev2Feed as RssFeed

from ..models import Post


class LatestEntriesFeed(Feed):
    # TODO: find a way to get this from the context processor instead of hardcoding it here
    title = "Diary of a Polymath"
    description = "A personal knowledge journal and publishing space."

    @property
    def link(self):
        return reverse("blog:index")

    def items(self):
        return Post.objects.get_published_posts()

    def item_title(self, item):
        return f"{item.title} | {item.subtitle}"

    def item_description(self, item):
        return item.abstract

    def item_pubdate(self, item):
        return item.published_on

    def item_categories(self, item):
        return [tag.name for tag in item.tags.all()]

    def item_link(self, item):
        return reverse("blog:post", args=[item.slug])


class RssLatestPostsFeed(LatestEntriesFeed):
    feed_type = RssFeed


class AtomLatestPostsFeed(LatestEntriesFeed):
    feed_type = AtomFeed
