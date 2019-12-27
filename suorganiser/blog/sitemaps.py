from datetime import date
from math import log10

from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = "never"
    limit = 3

    def items(self):
        return Post.objects.published()

    def lastmod(self, post):
        return post.pub_date

    def priority(self, post):
        period = 90
        time_delta = date.today() - post.pub_date
        days = time_delta.total_seconds()
        if days == 0:
            return 1.0
        elif 0 < days <= period:
            normalised = (log10(period / days) / log10(period ** 2))
            normalised = round(normalised, 2)
            return normalised + 0.5
        else:
            return 0.5
