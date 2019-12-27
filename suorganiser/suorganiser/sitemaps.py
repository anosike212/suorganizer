from blog.sitemaps import PostSitemap
from organiser.sitemaps import (
    StartupSitemap, TagSitemap)
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class RootSitemap(Sitemap):
    priority = 0.6

    def items(self):
        return [
            'blog_post_list',
            'contact',
            'dj-auth:login',
            'organiser_startup_list',
            'organiser_tag_list',
        ]

    def location(self, url_name):
        return reverse(url_name)

sitemaps = {
    'roots': RootSitemap,
    'posts': PostSitemap,
    'startups': StartupSitemap,
    'tags': TagSitemap,
}