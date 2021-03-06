# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from post.views import post_index
from accounts.views import about_us


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', post_index, name='index'),
    url(r'^post/', include('post.urls')),
    url(r'^account/', include('accounts.urls')),
    url(r'^about-us/', about_us, name='about_us'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
