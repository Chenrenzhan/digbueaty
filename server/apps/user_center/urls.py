#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

# from server.apps.account import views

from views import *

urlpatterns = patterns('',
    url(r'^applystore/$', apply_store),
    # url(r'^add/item/$', add_item),
    # url(r'^add/item/action/$', add_item_action),

)