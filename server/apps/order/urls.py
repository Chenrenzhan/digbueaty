#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

# from server.apps.account import views

from views import *

urlpatterns = patterns('',
    url(r'^([%A-Za-z0-9]+?)/manage/$', order_manage),
    url(r'^([%A-Za-z0-9]+?)/pay/([%A-Za-z0-9]+?)/$', pay),
    url(r'^delivery/([%A-Za-z0-9]+?)/$', delivery),

)