#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.


class Store(models.Model):
    name = models.CharField(max_length=256)
    presentation = models.TextField(blank=True,default='')

    THE_TITLE_HAS_EXISTED = u"该店铺名已经被注册"

    @classmethod
    def is_store_exit(cls,name):
        try:
            store = cls.objects.get(name=name)
            return False
        except:
            return True
