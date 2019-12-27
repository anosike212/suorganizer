from django.contrib.sitemaps import (
    Sitemap, GenericSitemap)
from .models import Startup, Tag


tag_sitemap_dict = {
    'queryset': Tag.objects.all(),
}

TagSitemap = GenericSitemap(tag_sitemap_dict, changefreq = 'never')


class StartupSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Startup.objects.all()

    def lastmod(self, startup):
        if startup.newslink_set.exists():
            return (
                startup.newslink_set.latest().pub_date)
        else:
            return startup.founded_date
