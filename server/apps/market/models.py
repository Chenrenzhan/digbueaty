#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

import store

# Create your models here.


"""基本商品类"""
class Goods(models.Model):
    #所属商店
    store = models.ForeignKey(store.models.Store)
    #商品标题
    title = models.CharField(max_length = 128)
    #库存剩余量
    remain = models.IntegerField()
    #商品详情描述
    detail = models.TextField(blank=True)
    #已经下架
    is_sold_out = models.BooleanField(default=False)
    #价格
    price = models.FloatField()

    #获取所有主图
    def all_pic_set(self):
        return PicSet.objects.all().filter(goods=self)

class PicSet(models.Model):
    #所属商品
    commodity = models.ForeignKey(Goods)
    #图片描述
    alt = models.CharField(max_length = 128)
    #url
    url = models.URLField()

"""竞拍商品"""
class AuctionItem(models.Model):
    #商品
    goods = models.ForeignKey(Goods)
    #底价
    base_price = models.FloatField(blank=True)
    #竞拍当前最高价
    hightest_price = models.FloatField(blank=True)
    #订金
    subscription = models.FloatField(blank=True)
    #开始时间
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    #结束时间
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    #通知频率(秒)
    inform_rate = models.IntegerField()
    #是否流拍
    def is_abortive(self):
        try:
            auction_bid = AuctionBid.objects.all().filter(auction=self)
            return True
        except:
            return False

    #获取拍得者
    def get_highest_bid(self):
        bid_record = AuctionBid.objects.all().filter(auction=self)
        if(len(bid_record)==0):
            return None
        max_bid = bid_record[0]
        for item in bid_record:
            if(item.bid>max_bid.bid):
                max_bid = item
        return max_bid

    #价格达到商品原价格时立即购买
    def is_highter_price(self):
        if(self.hightest_price >= self.goods.price):
            return True
        else:
            return False



"""抽象订金基类"""
class BaseSubscriptionRecord(models.Model):
    #订金支付者
    buyer = models.ForeignKey('account.User')
    #账单id
    bill = models.ForeignKey('order.Bill')
    #结束
    is_done = models.BooleanField(default=False)

    class Meta:
        abstract = True

"""竞拍订金支付记录"""
class AuctionSubscriptionRecord(BaseSubscriptionRecord):
    #拍卖商品
    auction = models.ForeignKey(AuctionItem)
    #判断某人某竞拍有没付定金
    @classmethod
    def has_subscripted(cls, auction, user):
        try:
            record = cls.objects.all().filter(auction=auction,buyer=user)
            if(record.count()>0):
                return True
            return False
        except:
            return False

"""竞拍出价表"""
class AuctionBid(models.Model):
    #买家ID
    buyer = models.ForeignKey('account.User')
    #竞拍商品id
    auction = models.ForeignKey(AuctionItem)
    #出价额
    bid = models.FloatField()
    #是否拍得
    is_succeed = models.BooleanField(default=False)

"""团购商品"""
class GroupBuyingItem(models.Model):
    #商品id
    goods = models.ForeignKey(Goods)
    #最少团购数量
    min_num = models.IntegerField(default=0)
    #开始时间
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    #结束时间
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    #判断团购是否成立
    def is_successful(self):
        all_sub_records = GroupBuyingSubscriptionRecord.find_all_record(self)
        num = 0
        for item in all_sub_records:
            num = num + item.number
        if(num>self.min_num):
            return True
        return False


"""团购订金支付记录"""
class GroupBuyingSubscriptionRecord(BaseSubscriptionRecord):
    #拍卖商品
    group_buying = models.ForeignKey(GroupBuyingItem)
    #预定数量
    number = models.IntegerField()
    #获取某次团购所有记录
    @classmethod
    def find_all_record(cls,group_buying):
        return cls.objects.all().filter(group_buying=group_buying)







