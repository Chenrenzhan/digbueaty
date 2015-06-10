#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, HttpResponse

# Create your views here.

from models import *
from account.models import User

def notify_action(request, user_id):

    # user_id = request.GET['user_id']
    print(user_id)
    user=None
    try:
        user = User.objects.get(id=user_id)
    except Exception as e:
        print(e)

    inform_list=None
    try:
        inform_list=Inform.objects.filter(to=user, has_read=False)
    except Exception as e:
        print(e)
    print(inform_list)
    for inform in inform_list:
        print(inform.has_read)
        inform.has_read = True
        print(inform.has_read)
        try:
            inform.save()
        except Exception as e:
            print(e)
        print(inform.has_read)

    return HttpResponse("result")
    # return HttpResponseRedirect('/')