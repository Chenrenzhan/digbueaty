#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from action import *
from models import *
from account.models import User, Seller

from server.action import get_header_inform

import datetime, time

# Create your views here.


def noaccount_item_yikoujia(request, type, item_id):
    goods=None
    pic=None
    try:
        goods=Goods.objects.get(id=item_id)

        pic=PicSet.objects.get(goods=goods)
        # pass
    except Exception as e:
        print(e)
    item = getItem(goods, type)
    good = {'item':item, 'pic':pic}
    variable = {'goods':good}
    return render_to_response('noaccount_item_yikoujia.html', variable, context_instance=RequestContext(request))


def noaccount_item_auction(request, type, item_id):
    goods=None
    pic=None
    auction=None
    try:
        goods=Goods.objects.get(id=item_id)

        pic=PicSet.objects.get(goods=goods)
        auction = AuctionItem.objects.get(goods=goods)
    except Exception as e:
        print(e)
    print(goods)
    item = getItem(goods, type)
    good = {'item':item, 'pic':pic}
    variable = { 'goods':good, 'auction':auction}
    return render_to_response('noaccount_item_auction.html', variable, context_instance=RequestContext(request))


def noaccount_item_groupbuy(request, type, item_id):
    goods=None
    pic=None
    groupbuy=None
    try:
        goods=Goods.objects.get(id=item_id)

        pic=PicSet.objects.get(goods=goods)
        groupbuy = GroupBuyingItem.objects.get(goods=goods)
    except Exception as e:
        print(e)
    item = getItem(goods, type)
    good = {'item':item, 'pic':pic}
    variable = {'goods':good, 'groupbuy':groupbuy}
    return render_to_response('noaccount_item_groupbuy.html', variable, context_instance=RequestContext(request))
