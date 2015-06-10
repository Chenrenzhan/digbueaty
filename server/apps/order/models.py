#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

import datetime

import account
import store
import market

# Create your models here.



#账单
class Bill(models.Model):
    #账单总额
    total_amounts = models.FloatField(blank=True)
    #生成时间
    gtime = models.DateTimeField(auto_now=False, auto_now_add=False)
    #有效付款时间
    # deadline = models.DateTimeField(auto_now=False, auto_now_add=False)
    #支付时间
    paytime = models.DateTimeField(auto_now=False, auto_now_add=False)
    #自动转移时间
    # auto_confirm_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    #是否已经支付
    has_payed = models.BooleanField(default=False)
    #是否已经确认转移
    # has_confirm = models.BooleanField(default=False)
    #是否退还
    has_return = models.BooleanField(default=False)


#订单
class Order(models.Model):
    #订单编码，组成：前8位表示当天日期，后5表示一天按顺序编号
    # order_num = models.CharField(max_length=13, primary_key=True)
    #订单所属买家
    buy_user = models.ForeignKey(account.models.User, related_name='buy_user')
    #订单所属卖家
    sell_user = models.ForeignKey(account.models.User, related_name='sell_user')
    #所属店铺
    store = models.ForeignKey(store.models.Store)
    #账单
    bill = models.ForeignKey(Bill)
    #订单生成时间
    gtime = models.DateTimeField(auto_now=False, auto_now_add=False)
    #是否发货
    has_deliver = models.BooleanField(default=False)
    #是否确认收货
    has_confirm = models.BooleanField(default=False)
    #收货邮箱地址
    mail = models.EmailField(max_length=128)
    #收货人姓名
    name = models.CharField(max_length=50, default='')



    #发货
    def dliver(self):
        self.has_deliver = True
        self.save()

    #确认收货
    def confrim(self):
        self.has_confirm = True
        self.save()

    #获取所有item
    def all_items(self):
        return list(OrderItem.objects.all().filter(order=self))

    #添加item
    def add_item(self,item,num=1):
        try:
            order_item = OrderItem(commodity=item,order=self,number=num)
            order_item.save()
            self.update_bill()
        except:
            pass

    #删除item
    def del_item(self,item_id):
        try:
            order_item = OrderItem.objects.get(id=item_id)
            order_item.delete()
            self.update_bill()
        except:
            pass

    #更新账单
    def update_bill(self):
        item_list = self.all_items()
        sum_price = 0.0
        for item in item_list:
            sum_price = sum_price + item.price*item.number
        self.bill.total_amounts = sum_price
        self.bill.save()

    #直接设置账单额
    def set_price_direct(self,total_amounts):
        self.bill.total_amounts = total_amounts
        self.bill.save()


"""订单包括的商品"""
class OrderItem(models.Model):
    #商品id
    goods = models.ForeignKey(market.models.Goods)
    #订单id
    order = models.ForeignKey(Order)
    #数量
    number = models.IntegerField()
    #单价
    price = models.FloatField()
