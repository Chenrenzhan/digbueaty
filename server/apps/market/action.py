#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'chenrenzhan'
from account.models import User, Seller
from models import *
from order.models import Bill, Order, OrderItem
from notify.models import Inform
from notify.action import generate_deliver_notify, generate_pay_notify, refund_notify
from notify.action import groupbuy_success_notify, groupbuy_success_buyer_notify

import datetime
from django.db.models import Min, Max, Sum

def getItem(goods, type):
    if type == '1':
        try:
            return YiKouJiaItem.objects.get(goods=goods)
        except Exception as e:
            print(e)
    elif type == '2':
        try:
            return AuctionItem.objects.get(goods=goods)
        except Exception as e:
            print(e)
    else:
        try:
            return GroupBuyingItem.objects.get(goods=goods)
        except Exception as e:
            print(e)
    return None

def generate_bill(goods, has_paid, sum, seller, user):
    total_amounts = int(sum) * goods.price
    gtime = datetime.datetime.now()
    paytime = datetime.datetime.now()
    has_payed = False
    print('has_paid                                             aaaaaaaaaaaaa')
    print(has_paid)
    if (has_paid == '1'):
        # paytime = datetime.datetime.now()
        has_payed = True
        generate_deliver_notify(seller.user, user)
        print('has_paid                                             aaaaaaaaaaaaa')
        user.balance -= total_amounts
        user.save()
    else:
        generate_pay_notify(user)
    has_return = False
    try:
        return Bill.objects.create(total_amounts=total_amounts, gtime=gtime,
                                   paytime=paytime, has_payed=has_payed, has_return=has_return)
    except Exception as e:
        print(e)
        return None

def generate_order(bill, goods, buy_user, sell_user, mail, name):
    store = goods.store
    gtime = datetime.datetime.now()
    has_deliver = False
    has_confirm = False
    try:
        return Order.objects.create(buy_user=buy_user, sell_user=sell_user, store=store, bill=bill, gtime=gtime,
                                     has_deliver=has_deliver, has_confirm=has_confirm, mail=mail, name=name)
    except Exception as e:
        print(e)
        return None

def generate_orderItem(goods, order, sum):
    try:
        return OrderItem.objects.create(goods=goods, order=order, number=sum,
                                 price=goods.price)
    except Exception as e:
        print(e)
        return None


def refund(auction_item):
    record_set=None
    try:
        record_set = AuctionSubscriptionRecord.objects.filter(auction=auction_item, is_done=False,
                                                           bill__has_return__isnull=False)
    except Exception as e:
        print(e)
    for record in record_set:
        bill = record.bill
        bill.has_return=True
        bill.save()
        buyer = record.buyer
        buyer.balance += bill.total_amounts
        buyer.save()
        refund_notify(buyer, auction_item)

#获取最高出价表
def get_max_abid(auction):
    hightest_price = auction.hightest_price
    abid_list=None
    try:
        abid_list = AuctionBid.objects.filter(auction=auction, is_succeed=False, bid=hightest_price)
    except Exception as e:
        print(e)
    bid = 0.0
    return_abid=None
    for abid in abid_list:
        if abid.bid >= bid:
            bid = abid.bid
            return_abid =  abid
    return_abid.is_succeed=True
    return_abid.save()
    return return_abid


'''团购结束生成账单'''
def groupbuy_dead(groupbuy):
    record_list=None
    try:
        record_list=GroupBuyingSubscriptionRecord.objects.filter(group_buying=groupbuy)
    except Exception as e:
        print(e)

    for record in record_list:
        #出价额
        # bid = auction_bid.bid
        #数量
        sum = record.number
        #订金
        subscription = groupbuy.subscription

        price = groupbuy.price
        total = (price - subscription) * sum
        gtime = datetime.datetime.now()
        paytime = datetime.datetime.now()
        has_payed = False
        has_return = False

        bill=None
        try:
            bill = Bill.objects.create(total_amounts=total, gtime=gtime, paytime=paytime,
                                       has_payed=has_payed, has_return=has_return)
        except Exception as e:
            print(e)

        buyer=record.buyer
        sell_user=None
        goods=groupbuy.goods
        seller=None
        try:
            seller = Seller.objects.get(store=goods.store)
            sell_user = seller.user
        except Exception as e:
            print(e)

        order=None
        try:
            order=Order.objects.create(buy_user=buyer, sell_user=sell_user, store=goods.store,
                                       bill=bill, gtime=gtime, has_deliver=False, has_confirm=False,
                                       mail='13631261719@163.com', name='chenrenzhan')
        except Exception as e:
            print(e)

        order_item=None
        try:
            order_item = OrderItem.objects.create(goods=goods, order=order, number=sum, price=price)
        except Exception as e:
            print(e)

        groupbuy_success_notify(buyer, groupbuy)
        groupbuy_success_buyer_notify(buyer, groupbuy)