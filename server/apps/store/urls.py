#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

# from server.apps.account import views

from views import *

urlpatterns = patterns('',
    url(r'^edit/item/$', edit_item),

)