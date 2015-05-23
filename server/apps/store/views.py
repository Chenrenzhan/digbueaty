#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
# from django.template.context_processors import csrf
from django.middleware import csrf

# Create your views here.
from models import *

def edit_item(request):

    return render_to_response('edit_item.html', context_instance=RequestContext(request))