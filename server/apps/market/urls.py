#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

# from server.apps.account import views

from views import *
from noaccount_views import *

urlpatterns = patterns('',
    # url(r'^manage/([%A-Za-z0-9]+?)/$', store_manage),
    url(r'^item/yikoujia/([%A-Za-z0-9]+?)/([%A-Za-z0-9]+?)/$', item_yikoujia),
    url(r'^item/auction/([%A-Za-z0-9]+?)/([%A-Za-z0-9]+?)/$', item_auction),
    url(r'^item/groupbuy/([%A-Za-z0-9]+?)/([%A-Za-z0-9]+?)/$', item_groupbuy),

    #一口价购买
    url(r'^item/yikoujia/([%A-Za-z0-9]+?)/([%A-Za-z0-9]+?)/([%A-Za-z0-9]+?)/buy/$', buy),
    url(r'^([%A-Za-z0-9]+?)/order/([%A-Za-z0-9]+?)/([%A-Za-z0-9]+?)/$', order_yikoujia),
    url(r'^([%A-Za-z0-9]+?)/order/([%A-Za-z0-9]+?)/([%A-Za-z0-9]+?)/action/$', order_yikoujia_action),
    url(r'^([%A-Za-z0-9]+?)/order/([%A-Za-z0-9]+?)/([%A-Za-z0-9]+?)/pay/$', pay_yikoujia),

    #竞拍
    url(r'^item/auction/([%A-Za-z0-9]+?)/([%A-Za-z0-9]+?)/action/$', item_auction_auction),
    url(r'^item/auction/([%A-Za-z0-9]+?)/([%A-Za-z0-9]+?)/dead/action/$', auction_dead_action),

    #竞拍
    url(r'^item/groupbuy/([%A-Za-z0-9]+?)/([%A-Za-z0-9]+?)/action/$', item_groupbuy_auction),
    url(r'^item/groupbuy/([%A-Za-z0-9]+?)/([%A-Za-z0-9]+?)/dead/action/$', groupbuy_dead_action),

    #没账户下的商品界面url
    url(r'^noaccount/item/yikoujia/([%A-Za-z0-9]+?)/([%A-Za-z0-9]+?)/$', noaccount_item_yikoujia),
    url(r'^noaccount/item/auction/([%A-Za-z0-9]+?)/([%A-Za-z0-9]+?)/$', noaccount_item_auction),
    url(r'^noaccount/item/groupbuy/([%A-Za-z0-9]+?)/([%A-Za-z0-9]+?)/$', noaccount_item_groupbuy),
)