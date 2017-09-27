# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import *

app_name = 'accounts'

urlpatterns = [
    url(r'^$', article, name='article'),
    url(r'^(?P<slug>[\w-]+)/update/$', article_update, name='article_update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', article_delete, name='article_delete'),

    url(r'^category/$', category, name='category'),
    url(r'^category/(?P<slug>[\w-]+)/update/$', category_update, name='category_update'),
    url(r'^category/(?P<slug>[\w-]+)/delete/$', category_delete, name='category_delete'),

    url(r'^tag/$', tag, name='tag'),
    url(r'^tag/(?P<slug>[\w-]+)/update/$', tag_update, name='tag_update'),
    url(r'^tag/(?P<slug>[\w-]+)/delete/$', tag_delete, name='tag_delete'),

    url(r'^login/$', login_view, name='login'),
    url(r'^register/$', register_view, name='register'),
    url(r'^logout/$', logout_view, name='logout'),

]