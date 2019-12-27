"""suorganiser URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from organiser.urls import (
    tag as tag_urls,
    startup as startup_urls,
    newslink as newslink_urls)
from blog import urls as blog_urls
from .views import redirect_root
from contact import urls as contact_urls
from django.contrib.flatpages import urls as flatpages_urls
from user import urls as user_urls
from django.conf import settings
from django.conf.urls.static import static
from blog.feeds import AtomPostFeed, Rss2PostFeed
from django.contrib.sitemaps.views import (
    index as site_index_view,
    sitemap as sitemap_view)
from .sitemaps import sitemaps as sitemaps_dict
from organiser.views import Test

admin.site.site_header = "Startup Organiser Admin"
admin.site.site_title = "Startup Organiser Site Admin"
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

sitenews = [
    url(r'^atom/$',
        AtomPostFeed(),
        name = "blog_atom_feed"),
    url(r'^rss/$',
        Rss2PostFeed(),
        name = "blog_rss_feed"),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^sample\.json$', Test.as_view(), name = "my_json"),
    url(r'^$', redirect_root),
    url(r'^blog/', include(blog_urls)),
    url(r'^contact/', include(contact_urls)),
    url(r'^tag/', include(tag_urls)),
    url(r'^startup/', include(startup_urls)),
    url(r'^newslink/', include(newslink_urls)),
    url(r'^user/', include(user_urls, namespace = "dj-auth")),
    url(r'^sitenews/', include(sitenews)),
    url(r'^sitemap\.xml$',
        site_index_view,
        {
            'sitemaps': sitemaps_dict,
            'sitemap_url_name': 'sitemap-section',
        },
        name = 'sitemap'),
    url(r'^sitemap-(?P<section>.+)\.xml$',
        sitemap_view,
        {'sitemaps': sitemaps_dict},
        name = 'sitemap-section'),
    # url(r'^', include(flatpages_urls)),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
    url(r'^__debug__', include(debug_toolbar.urls))
]
