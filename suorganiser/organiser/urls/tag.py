from django.conf.urls import url  
from organiser.views import (
    tag_create, TagUpdate, TagDelete,
    tag_list, TagDetail, tag_page_list)

urlpatterns = [
    url(r'^$', 
        tag_list,
        name = "organiser_tag_list"),
    url(r'^(?P<page_number>\d+)/$',
        tag_page_list,
        name = "organiser_tag_page"),
    url(r'^create/$',
        tag_create,
        name = "organiser_tag_create"),
    url(r'^(?P<slug>[\w\-]+)(/)?$',
        TagDetail.as_view(), 
        name = "organiser_tag_detail"),
    url(r'^(?P<slug>[\w\-]+)/update/$',
        TagUpdate.as_view(),
        name = "organiser_tag_update"),
    url(r'^(?P<slug>[\w\-]+)/delete/$',
        TagDelete.as_view(), 
        name = "organiser_tag_delete"),
]