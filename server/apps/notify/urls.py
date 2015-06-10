#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

# from server.apps.account import views

from views import *

urlpatterns = patterns('',
    # url(r'^manage/([%A-Za-z0-9]+?)/$', store_manage),
    url(r'^([%A-Za-z0-9]+?)/action/$', notify_action),
)