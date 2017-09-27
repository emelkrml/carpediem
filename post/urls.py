# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import *

app_name= 'post'

urlpatterns = [
    # url(r'^index/$', post_index, name='index'),
    url(r'^create/$', post_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/update/$', post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete, name='delete'),
    url(r'^category/(?P<slug>[\w-]+)/$', category_detail, name='category_detail'),
    url(r'^tag/(?P<slug>[\w-]+)/$', tag_detail, name='tag_detail'),
]