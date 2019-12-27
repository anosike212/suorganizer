from django.conf.urls import url
from organiser.views import ( 
    NewsLinkCreate, NewsLinkUpdate, NewsLinkDelete)

urlpatterns = [
    url(r'^create/$',
        NewsLinkCreate.as_view(),
        name = "organiser_newslink_create"),
    url(r'^delete/(?P<pk>\d)/$',
        NewsLinkDelete.as_view(),
        name = "organiser_newslink_delete"),
    url(r'^update/(?P<pk>\d)/$',
        NewsLinkUpdate.as_view(),
        name = "organiser_newslink_update"),
]