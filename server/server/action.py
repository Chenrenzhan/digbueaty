#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'chenrenzhan'

from account.models import User, Seller
from notify.models import Inform

def get_header_inform(request):
    has_store = False
    seller = None
    host = request.get_host()
    notify = None
    print(host)
    if ( 'mail' in request.session):
        mail = request.session['mail']
        user = User.objects.get(mail=mail)
        try:
            seller = Seller.objects.get(user=user)
            has_store = True
        except:
            has_store = False
    try:
        notify = Inform.objects.filter(to=user, has_read=False)
    except Exception as e:
        print(e)
    notifys={'notify':notify, 'len':len(notify)}
    header_inform = {'user': user, 'has_store': has_store, 'seller': seller, 'notifys': notifys}
    return header_inform