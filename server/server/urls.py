#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
# from django.contrib import admin

# from apps import account
# from account.views import *
# print('aaaa   ' + apps.account)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),

    url(r'^account/',include('account.urls')),

    url(r'^store/',include('store.urls')),
    # url(r'^account/',signup),
)
