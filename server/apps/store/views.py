#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from action import *

# Create your views here.
from models import *
from market.models import Goods, PicSet,YiKouJiaItem, AuctionItem, GroupBuyingItem
from account.models import User, Seller

from server.action import get_header_inform

def store_manage(request, store_id):

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

        variable = {'user':user, 'has_store': has_store, 'seller': seller,'store_id':store_id}
        # variable = {}
        return render_to_response('store_manage.html', variable, context_instance=RequestContext(request))
    return render_to_response('index.html',context_instance=RequestContext(request))

def store_item(request, store_id):
    header_inform = get_header_inform(request)

    try:
        store=Store.objects.get(id=store_id)
        print(store)
        goods_list=Goods.objects.filter(store=store)
        print(goods_list)
        goods=[]
        yikoujia_list=[]
        auction_list=[]
        group_buy_list=[]
        for good in goods_list:
            print(good)
            pic=None
            try:
                pic=PicSet.objects.get(goods=good)
            except Exception as e:
                print(e)
            print(pic)
            # goods.append({'item':good, 'pic':pic})
            try:
                yikoujia=YiKouJiaItem.objects.get(goods=good)
                yikoujia_list.append({'item':yikoujia, 'pic':pic})
            except Exception as e:
                print(e)
            try:
                auction=AuctionItem.objects.get(goods=good)
                auction_list.append({'item':auction, 'pic':pic})
            except Exception as e:
                print(e)
            try:
                group_buy=GroupBuyingItem.objects.get(goods=good)
                group_buy_list.append({'item':group_buy, 'pic':pic})
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)
    variable = {'user':header_inform['user'], 'has_store': header_inform['has_store'],
                'seller': header_inform['seller'],'notifys':header_inform['notifys'],
                'yikoujia_list':yikoujia_list, 'auction_list':auction_list, 'group_buy_list':group_buy_list}
    print(variable)
    return render_to_response('store_item.html', variable, context_instance=RequestContext(request))


def add_item(request, store_id):
    header_inform = get_header_inform(request)

    variable = {'user':header_inform['user'], 'has_store': header_inform['has_store'],
                 'seller': header_inform['seller'],'notifys':header_inform['notifys'],
                'store_id':store_id}

    return render_to_response('store_additem.html', variable, context_instance=RequestContext(request))


def add_item_action(request,store_id):
    print('add')
    store_id = request.POST['store_id']
    title = request.POST['title']
    detail = request.POST['detail']
    price = request.POST['price']
    remain = request.POST['remain']
    # good_type = request.POST['radio']
    good_type = 6
    #通过request.REQUEST.getlist取到list形式的提交结果
    type_list = request.REQUEST.getlist('checkbox')
    print(type_list)
    if remain == '':
        remain = '0'
    print('remain   ' + remain)
    print('store_id  ' + store_id)
    store = None
    goods = None
    try:
        store = Store.objects.get(id = store_id)
    except Exception as e:
        print(e)
    try:
        goods = Goods.objects.create(store=store, title=title, remain=remain, detail=detail, is_sold_out=False,
                             price=price, goods_type=good_type)
        sort_goods(request, goods, type_list)
    except Exception as e:
        print(e)
    print(store)
    print(goods)
    save_pic(request, goods)
    print('title      ' + store_id)
    url = '/store/'+store_id+'/'
    return HttpResponseRedirect(url)




def edit_item(request, store_id, item_id):

    header_inform = get_header_inform(request)


    goods=None
    pic=None
    yikoujia=None
    auction=None
    group_buy=None
    try:
        goods = Goods.objects.get(id=item_id)
        pic = PicSet.objects.get(goods=goods)
        try:
             yikoujia=YiKouJiaItem.objects.get(goods=goods)
        except:
            pass
        try:
            auction=AuctionItem.objects.get(goods=goods)
        except:
            pass
        try:
            group_buy=GroupBuyingItem.objects.get(goods=goods)
        except:
            pass
    except Exception as e:
        print(e)


    variable = {'user':header_inform['user'], 'has_store': header_inform['has_store'],
                'seller': header_inform['seller'],'notifys':header_inform['notifys'],
                'store_id':store_id,'goods':goods,'pic':pic,'yikoujia':yikoujia,
                'auction':auction, 'group_buy':group_buy}
    print(variable)

    return render_to_response('store_edititem.html', variable, context_instance=RequestContext(request))


def edit_item_action(request, store_id, item_id):

    print('add')
    # store_id = request.POST['store_id']
    title = request.POST['title']
    detail = request.POST['detail']
    price = request.POST['price']
    remain = request.POST['remain']
    # good_type = request.POST['radio']
    good_type = 6
    #通过request.REQUEST.getlist取到list形式的提交结果
    type_list = request.REQUEST.getlist('checkbox')
    print(type_list)
    if remain == '':
        remain = '0'

    store = None
    goods = None
    try:
        goods=Goods.objects.get(id=item_id)
        delete_item(goods)
        goods.title=title
        goods.detail=detail
        goods.price=price
        goods.remain=remain
        goods.save()
        # sort_goods(request, goods, type_list)
    except Exception as e:
        print(e)
    sort_goods(request, goods, type_list)
    url = '/store/'+store_id+'/'
    return HttpResponseRedirect(url)
