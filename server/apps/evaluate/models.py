#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

from market.models import Goods
import market

# Create your models here.

"""评论"""
class Evaluation(models.Model):
    #评论商品
    goods = models.ForeignKey(market.models.Goods)
    #评论正文
    text = models.TextField()
    #评论时间
    gtime = models.DateTimeField()
    #额外评价指标
    extend = models.TextField(blank=True)
    #评论者
    eval_id = models.IntegerField()
    #被评论者
    evaled_id = models.IntegerField()
    #评论类型
    eval_type = models.CharField(max_length=16)

    # def get_all_addition_eval(self):
    #     return list(AdditionEval.objects.filter(aeval=self))