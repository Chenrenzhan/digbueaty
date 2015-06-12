#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect


from action import *
from models import *
from account.models import User, Seller

from server.action import get_header_inform
from order.models import Bill, Order, OrderItem
from notify.action import pay_left_notify, auction_dead_notify,generate_deliver_notify
from notify.action import  groupbuy_success_notify, groupbuy_success_buyer_notify
import datetime, time

# Create your views here.


def item_yikoujia(request, type, item_id):
    header_inform = get_header_inform(request)
    print(header_inform)
    goods=None
    pic=None
    try:
        goods=Goods.objects.get(id=item_id)

        pic=PicSet.objects.get(goods=goods)
        # pass
    except Exception as e:
        print(e)
    print(goods)
    item = getItem(goods, type)
    good = {'item':item, 'pic':pic}
    print(type)
    print(type == '1')
    print(good)
    variable = {'user':header_inform['user'], 'has_store': header_inform['has_store'],
                'seller': header_inform['seller'],'notifys':header_inform['notifys'],
                'goods':good}
    return render_to_response('item_yikoujia.html', variable, context_instance=RequestContext(request))

def buy(request, type, item_id, user_id):
    variable=None

    sum = request.POST['sum']
    request.session['sum'] = sum
    print(sum)
    url='/market/'+ user_id +'/order/'+ type + '/' + item_id + '/'
    return HttpResponseRedirect(url)
    # return render_to_response('order_yikoujia.html', variable, context_instance=RequestContext(request))


def order_yikoujia(request, user_id, type, item_id):
    header_inform = get_header_inform(request)

    goods=None
    pic=None
    sum='0'
    try:
        goods=Goods.objects.get(id=item_id)
    except Exception as e:
        print(e)

    try:
        pic=PicSet.objects.get(goods=goods)
    except Exception as e:
        print(e)
    if 'sum' in request.session:
        sum=request.session['sum']
    total = goods.price * int(sum)
    good={'item':goods, 'pic':pic}
    variable = {'user':header_inform['user'], 'has_store': header_inform['has_store'],
                'seller': header_inform['seller'],'notifys':header_inform['notifys'],
                'goods':good,  'sum':sum, 'total':total}
    return render_to_response('order_yikoujia.html', variable, context_instance=RequestContext(request))





def order_yikoujia_action(request, user_id, type, item_id):
    mail = request.POST['consignee_mail']
    name = request.POST['consignee_name']
    print(mail + '  ' + name)
    sum='0'
    if 'sum' in request.session:
        sum=request.session['sum']
    has_paid=request.POST['has_paid']
    print('has_paid' + has_paid)
    buy_user=None
    sell_user=None
    goods=None
    seller=None
    try:
        buy_user=User.objects.get(id=user_id)
    except Exception as e:
        print(e)
    try:
        goods=Goods.objects.get(id=item_id)
    except Exception as e:
        print(e)
    try:
        seller = Seller.objects.get(store=goods.store)
        sell_user = seller.user
    except Exception as e:
        print(e)

    bill = generate_bill(goods, has_paid, sum, seller, buy_user)

    order = generate_order(bill, goods, buy_user, sell_user, mail, name)

    orderItem = generate_orderItem(goods, order, sum)

    generate_deliver_notify(seller, buy_user)

    if 'sum' in request.session:
        del request.session['sum']

    url='/index/'+ user_id + '/'
    return HttpResponseRedirect(url)


def pay_yikoujia(request, user_id, type, item_id):
    variable=None


    return render_to_response('pay_yikoujia.html', variable, context_instance=RequestContext(request))
    # return HttpResponseRedirect(('/index/'+user_id))


def item_auction(request, type, item_id):
    header_inform = get_header_inform(request)
    goods=None
    pic=None
    auction=None
    try:
        goods=Goods.objects.get(id=item_id)

        pic=PicSet.objects.get(goods=goods)

        auction = AuctionItem.objects.get(goods=goods)
    except Exception as e:
        print(e)
    item = getItem(goods, type)
    good = {'item':item, 'pic':pic}

    variable = {'user':header_inform['user'], 'has_store': header_inform['has_store'],
                'seller': header_inform['seller'],'notifys':header_inform['notifys'],
                'goods':good, 'auction':auction}
    return render_to_response('item_auction.html', variable, context_instance=RequestContext(request))

def item_auction_auction(request, buyer_id, item_auction_id):
    print('item_auction_action')
    sum = int(request.GET['sum'])
    bid = float(request.GET['bid'])

    auction_item=None
    buyer=None
    try:
        auction_item = AuctionItem.objects.get(id=item_auction_id)
        refund(auction_item)
    except Exception as e:
        print(e)
    try:
        buyer = User.objects.get(id=buyer_id)
    except Exception as e:
        print(e)

    total_amounts = sum * bid
    gtime = datetime.datetime.now()
    paytime = datetime.datetime.now()
    has_payed = True
    has_return = False

    bill=None
    try:
        bill = Bill.objects.create(total_amounts=total_amounts, gtime=gtime, paytime=paytime,
                                   has_payed=has_payed, has_return=has_return)
    except Exception as e:
        print(e)

    auction_bid=None
    try:
        auction_bid = AuctionBid.objects.create(buyer=buyer, auction=auction_item,bid=bid, is_succeed=False, sum=sum)
    except Exception as e:
        print(e)

    auction_subscript_record=None
    try:
        auction_subscript_record=AuctionSubscriptionRecord.objects.create(buyer=buyer,
                                 bill=bill, is_done=False, auction=auction_item)
    except Exception as e:
        print(e)

    buyer.balance -= total_amounts
    buyer.save()
    auction_item.hightest_price = bid
    auction_item.save()


    print(sum.__class__)
    print(bid)

    return HttpResponse("result")
    # pass

#竞拍时间截止
def auction_dead_action(request, buyer_id, item_auction_id):
    print('auction_dead_action')
    auction_item=None
    buyer=None
    try:
        auction_item = AuctionItem.objects.get(id=item_auction_id)
        refund(auction_item)
    except Exception as e:
        print(e)
    try:
        buyer = User.objects.get(id=buyer_id)
    except Exception as e:
        print(e)

    auction_bid = get_max_abid(auction_item)

    #出价额
    bid = auction_bid.bid
    #数量
    sum = auction_bid.sum
    #订金
    subscription = auction_item.subscription

    total = (bid - subscription) * sum
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

    sell_user=None
    goods=auction_item.goods
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
        order_item = OrderItem.objects.create(goods=goods, order=order, number=sum, price=bid)
    except Exception as e:
        print(e)

    pay_left_notify(buyer, auction_item)
    auction_dead_notify(buyer, auction_item)

    return HttpResponse('result')


def item_groupbuy(request, type, item_id):
    header_inform = get_header_inform(request)
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
    variable = {'user':header_inform['user'], 'has_store': header_inform['has_store'],
                'seller': header_inform['seller'],'notifys':header_inform['notifys'],
                'goods':good, 'groupbuy':groupbuy}
    return render_to_response('item_groupbuy.html', variable, context_instance=RequestContext(request))


def item_groupbuy_auction(request, buyer_id, item_groupbuy_id):
    print('item_auction_action')
    sum = int(request.GET['sum'])
    #
    groupbuy_item=None
    buyer=None
    try:
        groupbuy_item = GroupBuyingItem.objects.get(id=item_groupbuy_id)
    #     refund(auction_item)
    except Exception as e:
        print(e)
    try:
        buyer = User.objects.get(id=buyer_id)
    except Exception as e:
        print(e)
    groupbuy_item.cur_sum = sum
    groupbuy_item.save()
    total_amounts = sum * groupbuy_item.price
    gtime = datetime.datetime.now()
    paytime = datetime.datetime.now()
    has_payed = True
    has_return = False

    bill=None
    try:
        bill = Bill.objects.create(total_amounts=total_amounts, gtime=gtime, paytime=paytime,
                                   has_payed=has_payed, has_return=has_return)
    except Exception as e:
        print(e)


    groupbuy_subscript_record=None
    try:
        groupbuy_subscript_record=GroupBuyingSubscriptionRecord.objects.create(group_buying=groupbuy_item,
                                 buyer=buyer, number=sum, bill=bill, is_done=False)
    except Exception as e:
        print(e)
    #
    buyer.balance -= total_amounts
    buyer.save()
    groupbuy_item.goods.remain -= sum
    groupbuy_item.save()


    return HttpResponse("result")

#团购时间截止
def groupbuy_dead_action(request, buyer_id, item_groupbuy_id):
    print('auction_dead_action')
    groupbuy_item=None
    buyer=None
    try:
        groupbuy_item = GroupBuyingItem.objects.get(id=item_groupbuy_id)
    #     refund(auction_item)
    except Exception as e:
        print(e)
    try:
        buyer = User.objects.get(id=buyer_id)
    except Exception as e:
        print(e)

    groupbuy_dead(groupbuy_item)

    return HttpResponse('result')

