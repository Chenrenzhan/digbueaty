#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

# from server.apps.account import views

from views import *

urlpatterns = patterns('',
    url(r'^signup/$', signup),
    url(r'^signup/action/$', signup_action),
    url(r'^signup/error/$', signup_error),
    url(r'^logout', logout),
    url(r'^login/$', login),
    url(r'^login/action/$', login_action),
    url(r'^login/error/$', login_error),
    url(r'^logout/$', logout),
)