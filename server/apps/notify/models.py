#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

import account

# Create your models here.
"""消息类"""
class Inform(models.Model):
    #通知标题
    title = models.CharField(max_length = 128)
    #通知正文
    text = models.TextField()
    #通知对象
    to = models.ForeignKey(account.models.User)
    #通知生成时间
    gtime = models.DateTimeField(auto_now=True)
    #是否已读
    has_read = models.BooleanField(default=False)

    #获取所有发往user的通知
    @classmethod
    def find_all_inform(cls,user):
        return list(cls.objects.all().filter(to=user))

    #获取所有发完user的未读通知
    @classmethod
    def find_all_unread(cls,user):
        return list(cls.objects.all().filter(to=user,has_read=False))

    #设为已读
    def read(self):
        self.has_read = True
        self.save()