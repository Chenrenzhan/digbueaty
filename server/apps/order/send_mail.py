# -*- coding: utf-8 -*-
"""
mandrill_serder和smtp_sender
其中, mandrill_sender是使用了mandrill服务的, 即使不翻墙
也能使用gmail往外发邮件, 但是, 永远不到qq邮箱那里去
smtp_sender就是简单封装了smtp协议, 但是要求登陆你的发送邮箱, 也就是
不能使用gmail作为发送邮箱
一般来说, 都能发到QQ邮箱

例子:
sender1 = mandrill_sender(your_api_key)
#没写api_key就是用setting里面的
sender2 = smtp_sender('邮箱地址',
    '邮箱密码', 'smtp服务器,比如smtp.gmail.com',
    'smtp服务器的端口, 默认25')

message = {
    'html':u'HTML的邮件正文, 理论上是html文本都行',
    'text':u'也是正文, 但只有html为空的时候才有用',
    'subject':u'邮件主题',
    'from_email':u'来源邮箱, 当对方接到邮件的时候, from显示的就是这个',
    'from_name':u'呃, 就是显示的发信方的名字, 可以随便写',
    'to:[{'email':'1234@gmail.com'}]'#to是一个列表, 每个元素是一个目标地址
    }
sender1.send(message)
sender2.send(message)


"""

import mandrill
# import setting
import smtplib
import unittest
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

MANDRILL_API_KEY = 'eHPTmMlVBFpbtrP5zWuolQ'

class mandrill_sender:
    def __init__(self, _key=MANDRILL_API_KEY):
        self.client = mandrill.Mandrill(_key)

    def send(self,_message):
        self.client.messages.send(_message)
#发货
    def deliver(self):
        import base64
        from mail import mandrill_sender
        seller = Seller.objects.get(store=self.order.store).user
        encoded_string = None
        pic = PicSet.objects.get(commodity=self.commodity)
        file_name = pic.file_name()
        image_type = pic.type()

        with open(file_name,'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read())
        message = {
            'html':'<img src="cid:product" width="560px">',
            'subject':u'[淘美人发货邮件]您购买的%s已经到货, 敬请查收'%self.commodity.title,
            'from_email':seller.mail,
            'from_name':seller.uname,
            'to':[{'email':self.order.mail}],
            'images':[{'content':encoded_string,'type':image_type,'name':'product'}]
        }
        sender = mandrill_sender()
        sender.send(message)

