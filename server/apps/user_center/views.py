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
import json

from account.models import User, Seller
from store.models import Store

def index(request):
    #标记是否已经开了点,0表示未开
    has_store = False
    seller = None
    store = None
    host = request.get_host()
    print(host)
    if( 'mail' in request.session):
        mail = request.session['mail']
        # del request.session['mail']
        user = User.objects.get(mail=mail)
        # has_store = Seller.is_seller(user = user)
        try:
            seller = Seller.objects.get(user = user)
            # store = Store.objects.get
            has_store = True
        except:
            has_store = False
        print(user.uname)

        variable = {'user':user, 'has_store': has_store, 'seller': seller}
        return render_to_response('index.html', variable, context_instance=RequestContext(request))
    else:
        return render_to_response('index.html',context_instance=RequestContext(request))


    # user = User.objects.get(mail='12@c.com')
    # print(user.uname)
    # variable = {'user':user, 'has_store': False, 'seller': seller}
    # return render_to_response('index.html',variable, context_instance=RequestContext(request))


    # return render_to_response('index.html',context_instance=RequestContext(request))

def apply_store(request):
    is_success = False
    if 'information' in request.POST:
        inf_str = request.POST['information']
        print(inf_str)
        information = json.loads(inf_str)
        store_name = information['store_name']
        store_presentation = information['store_presentation']
        mail = information['mail']



        user = User.objects.get(mail = mail)
        print(user)

        try:
            Store.objects.get(name = store_name)
            print('qqqqqqqqqqqqqqqq')
            is_success = False
        except Exception as e:
            store = Store.objects.create(name = store_name, presentation = store_presentation)
            try:
                seller = Seller.objects.create(user = user, store = store)
                is_success = True
            except:
                is_success = False

            print('store')
            print(e)
        print(store_name)
    result = {"is_success": is_success}
    print(result)
    return HttpResponse(json.dumps(result))