#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
# from django.templates.context_processors import csrf
from django.middleware import csrf

# Create your views here.
import json

from account.models import User, Seller
from store.models import Store
from market.models import Goods, PicSet,YiKouJiaItem, AuctionItem, GroupBuyingItem
from action import items

from server.action import get_header_inform

def index(request):

    yikoujia_list=[]
    auction_list=[]
    group_buy_list=[]
    try:
        yikoujia_list=YiKouJiaItem.objects.all()
        auction_list=AuctionItem.objects.all()
        group_buy_list=GroupBuyingItem.objects.all()

    except Exception as e:
        print(e)


    # variable={'yikoujia_list':yikoujia_list, 'auction_list':auction_list, 'group_buy_list':group_buy_list}

    variable = {'yikoujia_list':items(yikoujia_list), 'auction_list':items(auction_list), 'group_buy_list':items(group_buy_list)}
    print(variable)
    return render_to_response('index.html',variable, context_instance=RequestContext(request))

def index_account(request, user_id):
    header_inform = get_header_inform(request)

    host = request.get_host()
    print(host)

    yikoujia_list=[]
    auction_list=[]
    group_buy_list=[]
    try:
        yikoujia_list=YiKouJiaItem.objects.all()
        auction_list=AuctionItem.objects.all()
        group_buy_list=GroupBuyingItem.objects.all()
    except Exception as e:
        print(e)

    variable = {'user':header_inform['user'], 'has_store': header_inform['has_store'],
                'seller': header_inform['seller'],'notifys':header_inform['notifys'],
                'yikoujia_list':items(yikoujia_list), 'auction_list':items(auction_list),
                'group_buy_list':items(group_buy_list)}
    return render_to_response('index_account.html', variable, context_instance=RequestContext(request))


def apply_store(request):
    is_success = False
    if 'information' in request.POST:
        inf_str = request.POST['information']
        print(inf_str)
        information = json.loads(inf_str)
        store_name = information['store_name']
        store_presentation = information['store_presentation']
        mail = information['mail']



        user = User.objects.get(mail = mail)
        print(user)
        if Seller.is_seller(user):
            is_success = False
        else:
            try:
                Store.objects.get(name = store_name)
                is_success = False
            except Exception as e:
                store = Store.objects.create(name = store_name, presentation = store_presentation)
                try:
                    seller = Seller.objects.create(user = user, store = store)
                    is_success = True
                except:
                    is_success = False

                print('store')
                print(e)
        print(store_name)
    result = {"is_success": is_success}
    print(result)
    return HttpResponse(json.dumps(result))