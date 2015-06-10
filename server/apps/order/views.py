#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from action import *


# Create your views here.
from server.action import get_header_inform
from account.models import User, Seller
from order.models import Order, OrderItem
# from action import *
from market.models import PicSet
from notify.action import generate_deliver_notify, generate_pay_notify, generate_has_delivery

from django.db.models.query_utils import Q

def order_manage(request, user_id):
    header_inform = get_header_inform(request)
    user = None
    try:
        user = User.objects.get(id=user_id)
    except Exception as e:
        print(e)
    order_list=None
    try:
        order_list = Order.objects.filter(Q(buy_user=user) | Q(sell_user=user))
    except Exception as e:
        print(e)

    buy_order = []
    sell_order = []
    for order in order_list:
        order_item=None
        try:
            order_item = OrderItem.objects.get(order=order)
        except Exception as e:
            print(e)
        goods=order_item.goods
        number = order_item.number
        price = order_item.price
        total = number * price
        pic=None
        try:
            pic = PicSet.objects.get(goods=goods)
        except Exception as e:
            print(e)

        if order.sell_user.id == long(user_id):
            sell_order.append({'order':order, 'goods':goods, 'pic':pic, 'price':price, 'sum':number, 'total':total})
        if order.buy_user.id == long(user_id):
            buy_order.append({'order':order, 'goods':goods,  'pic':pic, 'price':price, 'sum':number, 'total':total})
    print("sell_order")
    print(sell_order)
    variable = {'user':header_inform['user'], 'has_store': header_inform['has_store'],
                'seller': header_inform['seller'],'notifys':header_inform['notifys'],
                'buy_orders':buy_order, 'sell_orders':sell_order}
    return render_to_response('order_manage.html', variable, context_instance=RequestContext(request))


def pay(request, user_id, order_id):
    print('pay')
    user = None
    order = None
    try:
        user = User.objects.get(id=user_id)
    except Exception as e:
        print(e)
    try:
        order = Order.objects.get(id=order_id)
    except Exception as e:
        print(e)
    bill = order.bill
    total = bill.total_amounts
    user.balance -= total
    user.save()
    bill.has_payed = True
    bill.save()
    generate_deliver_notify(order.sell_user, user)
    # generate_pay_notify(order.sell_user)
    return HttpResponse("result")

# from send_mail import send_mail
def delivery(request, order_id):
    order=None
    try:
        order = Order.objects.get(id=order_id)
    except Exception as e:
        print(e)

    send_mail(order)
    order.has_deliver = True
    order.save()
    generate_has_delivery(order)
    return HttpResponse('success')