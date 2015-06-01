#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
# from django.contrib import admin

# from apps import account
# from account.views import *
# print('aaaa   ' + apps.account)
from apps.user_center.views import index

from settings import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':MEDIA_ROOT}),


    url(r'^index/',index),

    url(r'^account/',include('account.urls')),

    url(r'^store/',include('store.urls')),

    url(r'^usercenter/',include('user_center.urls')),
    # url(r'^account/',signup),
)
