from datetime import datetime
from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from django.utils.feedgenerator import (
    Atom1Feed, Rss201rev2Feed)
from .models import Post


class BasePostFeedMixin():
    title = "Latest Startup Organiser Blog Posts"
    link = reverse_lazy("blog_post_list")
    description = subtitle = (
        "Stay up to date on the "
        "hottest startup news.")
    
    def items(self):
        return Post.objects.published()[:10]
    
    def item_title(self, item):
        return item.formatted_title()

    def item_description(self, item):
        return item.short_text()


class AtomPostFeed(BasePostFeedMixin, Feed):
    feed_type = Atom1Feed


class Rss2PostFeed(BasePostFeedMixin, Feed):
    feed_type = Rss201rev2Feed
