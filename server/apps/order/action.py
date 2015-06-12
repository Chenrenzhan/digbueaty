#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mandrill
from models import Order, OrderItem
from market.models import PicSet
import base64
import os

from server.settings import BASE_DIR

MANDRILL_API_KEY = 'eHPTmMlVBFpbtrP5zWuolQ'
class mandrill_sender:
    def __init__(self, _key=MANDRILL_API_KEY):
        self.client = mandrill.Mandrill(_key)

    def send(self,_message):
        self.client.messages.send(_message)

def send_mail(order):
    order_item=None
    try:
        order_item = OrderItem.objects.get(order=order)
    except Exception as e:
        print(e)
    goods=None
    goods=order_item.goods
    buy_user=order.buy_user
    sell_user=order.sell_user
    pic=None
    try:
        pic = PicSet.objects.get(goods=goods)
    except Exception as e:
        print(e)
    encoded_string=None
    pic_url = pic.picUrl.url
    pic_path = (BASE_DIR +  pic_url).replace('\\','/');
    try:
        with open(pic_path,'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read())
    except Exception as e:
        print(e)
    try:
        message = {
                    'html':'<h1>%s</h1><img src="cid:product" width="560px">' % goods.title,
                    'text':u'您在淘美人购买的 %s 已经到货了，敬请查收' % goods.title ,
                    'subject':u'[淘美人发货邮件]您购买的 %s 已经到货, 敬请查收' % goods.title,
                    'from_email':sell_user.mail,
                    'from_name': sell_user.uname,
                    'to':[{'email':order.mail}],
                    'images':[{'content':encoded_string,'type':'image/png','name':'product'}],
                }
        sender = mandrill_sender()
        sender.send(message)
    except Exception as e:
        print(e)

    print('send mail finish')