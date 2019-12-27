from django.conf.urls import url
from organiser.views import (
    NewsLinkCreate, NewsLinkDelete, NewsLinkUpdate,
    StartupCreate, StartupUpdate, StartupDelete,
    StartupList, StartupDetail)
from organiser.feeds import (
    AtomStartupFeed, Rss2StartupFeed)

urlpatterns = [
    url(r'^$',
        StartupList.as_view(),
        name = "organiser_startup_list"),
    url(r'^create/$',
        StartupCreate.as_view(),
        name = 'organiser_startup_create'),
    url(r'^(?P<slug>[\w\-]+)/$',
        StartupDetail.as_view(),
        name = "organiser_startup_detail"),
    url(r'^(?P<slug>[\w\-]+)/update/$',
        StartupUpdate.as_view(),
        name = "organiser_startup_update"),
    url(r'^(?P<slug>[\w\-]+)/delete/$',
        StartupDelete.as_view(),
        name = "organiser_startup_delete"),
    url(r'^(?P<startup_slug>[\w\-]+)/atom/$',
        AtomStartupFeed(),
        name = "organiser_startup_atom_feed"),
    url(r'^(?P<startup_slug>[\w\-]+)/rss/$',
        Rss2StartupFeed(),
        name = "organiser_startup_rss_feed"),
    url(r'^(?P<startup_slug>[\w\-]+)/'
        r'add_article_link/$',
        NewsLinkCreate.as_view(),
        name = "organiser_newslink_create"),
    url(r'^(?P<startup_slug>[\w\-]+)/'
        r'(?P<newslink_slug>[\w\-]+)/'
        r'delete/$',
        NewsLinkDelete.as_view(),
        name = "organiser_newslink_delete"),
    url(r'^(?P<startup_slug>[\w\-]+)/'
        r'(?P<newslink_slug>[\w\-]+)/'
        r'update/$',
        NewsLinkDelete.as_view(),
        name = "organiser_newslink_update"),
]