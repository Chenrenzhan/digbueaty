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

"""注册"""
def signup(request):
    # c = {}
    # c.update(csrf(request))
    # render_to_response('signup.html')
    # return render_to_response('signup.html',c)
    return render_to_response('signup.html',context_instance=RequestContext(request))
    # HttpResponse('hello world!')

#页面信息处理
def signup_action(request):
    email = request.POST['email']

    if(User.is_inavailable_email(email)):
         # return render_to_response('signup_error',{'error': User.REPEATED_EMAIL},context_instance=RequestContext(request))
        return HttpResponseRedirect('/account/signup/error')
    else:
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create(mail = email, uname = username, password = password, balance = 100000000)
        print(user)
    print(email)
    request.session['mail'] = user.mail;

    #跳转到首页
    return HttpResponseRedirect('/index/')
    # return render_to_response('/index/',context_instance=RequestContext(request))

#注册错误页面
def signup_error(request):

    return render_to_response('signup.html',{'error': User.REPEATED_EMAIL},context_instance=RequestContext(request))


"""登录"""
def login(request):
    return render_to_response('login.html', context_instance=RequestContext(request))

#页面信息处理
def login_action(request):
    email = request.POST['email']
    password = request.POST['password']

    try:
        user = User.objects.get(mail = email)
        if(password == user.password):
            request.session['mail'] = user.mail
            return HttpResponseRedirect('/index/')
        else:
            return HttpResponseRedirect('/account/login/error')
    except:
        return HttpResponseRedirect('/account/login/error')



def login_error(request):

    return render_to_response('login.html',{'error': User.LOGIN_ERROR},context_instance=RequestContext(request))

"""登出"""
def logout(request):

    if 'mail' in request.session:
        del request.session['mail']
    return render_to_response('login.html',context_instance=RequestContext(request))