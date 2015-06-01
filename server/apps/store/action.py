#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'chenrenzhan'

from django.shortcuts import render_to_response
from django.http import HttpResponse

import os
from server.settings import BASE_DIR
from PIL import Image
import hashlib
import time
import datetime

from market.models import PicSet, YiKouJiaItem, AuctionItem, GroupBuyingItem

'''时间格式'''
TIME_FORM =  '%Y/%m/%d %H:%M'

'''保存上传图片'''
def save_pic(request, goods):
    try:
        reqfile = request.FILES['item_pic_file']#picfile要和html里面一致
        img = Image.open(reqfile)
        img.thumbnail((500,500),Image.ANTIALIAS)#对图片进行等比缩放

        name = get_md5_value(reqfile.name)
        name += str(time.time())
        name = 'media/'+ name + '.png'
        path = os.path.join(BASE_DIR, name).replace('\\','/')
        # re = img.save(path, 'png')#保存图片
        reqfile.name = path
        try:
            pic_set = PicSet.objects.create(goods=goods, picUrl=reqfile)
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)
        return HttpResponse("Error %s" % e)#异常，查看报错信息

'''返回字符串的MD5'''
def get_md5_value(src):
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest


def sort_goods(request, goods, type_list):
    print('sort_goods')
    print(goods)
    print(type_list)
    print('sort_goods')
    for type in type_list:
        print(type + '   :  ' +  type.__class__())
        if type == '1':
            yikoujia(request, goods)
        elif type == '2':
            auction(request, goods)
        elif type == '3':
            group_buy(request, goods)
        else:
            continue

'''一口价商品'''
def yikoujia(request, goods):
    print('yikoujia')
    try:
        return YiKouJiaItem.objects.create(goods=goods)
    except Exception as e:
        print(e)


'''竞拍商品'''
def auction(request, goods):
    #商品
    # goods = models.ForeignKey(Goods)
    #底价
    base_price = request.POST['auction_base_price']
    #竞拍当前最高价
    hightest_price = 0.00
    #订金
    subscription = request.POST['subscription']
    #开始时间
    start_time = request.POST['auction_start_time']
    #结束时间
    end_time = request.POST['auction_end_time']
    print(start_time)
    print(start_time.__class__())
    start_time=datetime.datetime.strptime(start_time,TIME_FORM)
    end_time=datetime.datetime.strptime(end_time,TIME_FORM)

    try:
        return AuctionItem.objects.create(goods=goods, base_price=base_price, hightest_price=hightest_price,
                                   subscription=subscription, start_time=start_time, end_time=end_time)
    except Exception as e:
        print(e)
        return None

'''团购商品'''
def group_buy(request, goods):
    #商品id
    # goods = models.ForeignKey(Goods)
    #团购价
    price = request.POST['group_buy_price']
    #最少团购数量
    min_num = request.POST['group_buy_sum']
    #开始时间
    start_time = request.POST['group_buy_start_time']
    #结束时间
    end_time = request.POST['group_buy_end_time']

    start_time=datetime.datetime.strptime(start_time,TIME_FORM)
    end_time=datetime.datetime.strptime(end_time,TIME_FORM)

    try:
        return GroupBuyingItem.objects.create(goods=goods, price=price, min_num=min_num,
                                       start_time=start_time, end_time=end_time)
    except Exception as e:
        return None
        print(e)