#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

# from server.apps.account import views

from views import *

urlpatterns = patterns('',
    # url(r'^manage/([%A-Za-z0-9]+?)/$', store_manage),
    url(r'^([%A-Za-z0-9]+?)/$', store_item),
    # url(r'^([%A-Za-z0-9]+?)/$', store_manage),
    url(r'^([%A-Za-z0-9]+?)/add/item/$', add_item),
    url(r'^([%A-Za-z0-9]+?)/add/item/action/$', add_item_action),
    url(r'^([%A-Za-z0-9]+?)/edit/item/([%A-Za-z0-9]+?)/$', edit_item),
    url(r'^([%A-Za-z0-9]+?)/edit/item/([%A-Za-z0-9]+?)/action/$', edit_item_action),

)