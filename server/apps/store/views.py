#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext

from action import *

# Create your views here.
from models import *
from market.models import Goods, PicSet
from account.models import User, Seller

def store_manage(request, store_name):

    if( 'mail' in request.session):
        mail = request.session['mail']
        user = User.objects.get(mail=mail)

        try:
            seller = Seller.objects.get(user = user)
            # store = Store.objects.get
            has_store = True
        except:
            has_store = False
        print(user.uname)

        variable = {'user':user, 'has_store': has_store, 'seller': seller,'store_name':store_name}
        # variable = {}
        return render_to_response('store_manage.html', variable, context_instance=RequestContext(request))
    return render_to_response('index.html',context_instance=RequestContext(request))


def add_item(request):


    return render_to_response('store_manage.html', context_instance=RequestContext(request))


def add_item_action(request):
    print('add')
    store_name = request.POST['store_name']
    title = request.POST['title']
    detail = request.POST['detail']
    price = request.POST['price']
    remain = request.POST['remain']
    good_type = request.POST['radio']
    #通过request.REQUEST.getlist取到list形式的提交结果
    type_list = request.REQUEST.getlist('checkbox')
    print(type_list)
    if remain == '':
        remain = '0'
    print('remain   ' + remain)
    print('store_name  ' + store_name)
    store = None
    goods = None
    try:
        store = Store.objects.get(name = store_name)
    except Exception as e:
        print(e)
    try:
        goods = Goods.objects.create(store=store, title=title, remain=remain, detail=detail,is_sold_out=False,
                             price=price, goods_type=good_type)
        sort_goods(request, goods, type_list)
    except Exception as e:
        print(e)
    print(store)
    print(goods)
    save_pic(request, goods)
    print('title      ' + store_name)
    return render_to_response('store_manage.html', context_instance=RequestContext(request))


def store_item(request, store_name):


    return render_to_response('store_item.html', context_instance=RequestContext(request))
