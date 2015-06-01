#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
# from account.views import User

class Store(models.Model):
    # user = models.ForeignKey('account.User')
    name = models.CharField(max_length=256)
    presentation = models.TextField(blank=True,default='')

