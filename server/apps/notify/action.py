#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'chenrenzhan'
from account.models import User, Seller
from models import *
from order.models import Bill, Order, OrderItem
from notify.models import Inform

import datetime

'''发货通知'''
def generate_deliver_notify(seller, user):
    sell_user = seller.user
    generate_deliver_notify(sell_user, user)

'''发货通知'''
def generate_deliver_notify(sell_user, user):
    title = u'发货通知'
    # 通知正文
    text = user.uname + u'已经下单并付款，请尽快发货！'
    #通知对象
    # to = seller.user
    #通知生成时间
    gtime = datetime.datetime.now()
    #是否已读
    has_read = False
    try:
        Inform.objects.create(title=title, text=text, to=sell_user,
                              gtime=gtime, has_read=has_read)
    except Exception as e:
        print(e)


'''付款通知'''
def generate_pay_notify(user):
    title = u'付款通知'
    # 通知正文
    text = u'您已经提交订单，请尽快付款！'
    #通知对象
    to = user
    #通知生成时间
    gtime = datetime.datetime.now()
    #是否已读
    has_read = False
    try:
        Inform.objects.create(title=title, text=text, to=to,
                              gtime=gtime, has_read=has_read)
    except Exception as e:
        print(e)


'''已经发货通知'''
def generate_has_delivery(order):
    sell_user = order.sell_user
    buy_user = order.buy_user
    store = order.store
    order_item = None
    try:
        order_item = OrderItem.objects.get(order=order)
    except Exception as e:
        print(e)
    goods = order_item.goods

    title = u'收货通知'
    text = u'您在 %s 购买的商品 %s , 卖家 %s 已经发货，请注意查收' % (store.name, goods.title, sell_user.uname)

    #通知对象
    to = buy_user
    #通知生成时间
    gtime = datetime.datetime.now()
    #是否已读
    has_read = False
    try:
        Inform.objects.create(title=title, text=text, to=to,
                              gtime=gtime, has_read=has_read)
    except Exception as e:
        print(e)


'''竞拍有更高价，退款通知'''
def refund_notify(buyer, auction):
    title = u'竞拍退还订金通知'
    text = u'您参与商品 %s 的竞拍有更高价出现，先退还您参加竞拍的订金，如需竞拍，请重新出更高价' % (auction.goods.title)
    #通知对象
    to = buyer
    #通知生成时间
    gtime = datetime.datetime.now()
    #是否已读
    has_read = False
    try:
        Inform.objects.create(title=title, text=text, to=to,
                              gtime=gtime, has_read=has_read)
    except Exception as e:
        print(e)

'''竞拍结束，提醒拍得者付尾款'''
def pay_left_notify(buyer, auction):
    title = u'竞拍成功通知'
    text = u'恭喜您成功竞拍得 %s ,请尽快付清尾款！' % (auction.goods.title)
    #通知对象
    to = buyer
    #通知生成时间
    gtime = datetime.datetime.now()
    #是否已读
    has_read = False
    try:
        Inform.objects.create(title=title, text=text, to=to,
                              gtime=gtime, has_read=has_read)
    except Exception as e:
        print(e)

'''竞拍结束通知'''
def auction_dead_notify(buyer, auction):
    title = u'竞拍结束通知'
    text = u'竞拍结束，用户 %s 成功拍得商品 %s' % (buyer.uname, auction.goods.title)
    #通知对象
    to = buyer
    #通知生成时间
    gtime = datetime.datetime.now()
    #是否已读
    has_read = False
    try:
        Inform.objects.create(title=title, text=text, to=to,
                              gtime=gtime, has_read=has_read)
    except Exception as e:
        print(e)


'''团购成功结束通知'''
def groupbuy_success_notify(buyer,groupbuy):
    title = u'团购成立通知'
    text = u'商品 %s 团购时间截止，数量已经达到要求' % (groupbuy.goods.title)
    #通知对象
    to = buyer
    #通知生成时间
    gtime = datetime.datetime.now()
    #是否已读
    has_read = False
    try:
        Inform.objects.create(title=title, text=text, to=to,
                              gtime=gtime, has_read=has_read)
    except Exception as e:
        print(e)

'''团购成功结束，参与团购者通知'''
def groupbuy_success_buyer_notify(buyer,groupbuy):
    title = u'团购成立通知'
    text = u'您参与的商品 %s 团购已经截止，数量已经达到要求，请尽快付清尾款' % (groupbuy.goods.title)
    #通知对象
    to = buyer
    #通知生成时间
    gtime = datetime.datetime.now()
    #是否已读
    has_read = False
    try:
        Inform.objects.create(title=title, text=text, to=to,
                              gtime=gtime, has_read=has_read)
    except Exception as e:
        print(e)