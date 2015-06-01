#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

from store.models import Store
import  store

"""用户信息"""
class User(models.Model):
    #用户名
    uname = models.CharField(max_length=64)
    #邮箱地址
    mail = models.EmailField(max_length=128)
    #密码
    password = models.CharField(max_length=256)
    #余额
    balance = models.IntegerField(blank=True)


    REPEATED_EMAIL = u'您的邮箱地址已被注册!'

    WRONG_PASSWORD = u'密码错误!'

    NONEXISTENT_ACCOUNT = u'账号不存在'

    @classmethod
    def is_available_email(cls,mail):
        if cls.objects.filter(mail=mail).count() == 0:
            return True
        return False

    #判断是否卖家
    def is_seller(self):
        return Seller.is_seller(self)


"""卖家"""
class Seller(models.Model):
    user = models.ForeignKey(User)
    #店铺
    # store = models.ForeignKey('store.Store')


    #判断是否已经是卖家
    @classmethod
    def is_seller(cls,user):
        try:
            seller = cls.objects.get(user=user)
            return True
        except:
            return False

