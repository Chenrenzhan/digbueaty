#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenrenzhan'

from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect

def signup(request):

    render_to_response('signup.html')