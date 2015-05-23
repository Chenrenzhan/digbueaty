#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Q

import account

# Create your models here.


"""小组类"""
class Group(models.Model):
    #小组名字
    title = models.CharField(max_length = 128)
    #小组描述
    description = models.TextField()
    #小组创始人
    founder = models.ForeignKey(account.models.User)

    #获取所有组员
    def all_member(self):
        ret = []
        group_member = list(GroupMember.objects.filter(group=self))
        for item in group_member:
            ret.append(item.user)
        return ret
    #添加组员
    def add_member(self,user):
        try:
            group_member = GroupMember.objects.get(group=self,user=user)
        except:
            group_member = GroupMember(group=self,user=user)
            group_member.save()

    #判断某user是不是某组成员
    @classmethod
    def is_member(cls,group,user):
        try:
            group_member = GroupMember.objects.get(group=group,user=user)
            return True
        except:
            return False

    #判断一个集合是否全是组员
    @classmethod
    def all_are_members(cls,group,user_set):
        flag = True
        for user in user_set:
            flag = cls.is_member(group,user)
        return flag

    #判断一个集合时候就是全部组员了
    @classmethod
    def are_all_members(cls,group,user_set):
        flag = True
        flag = cls.all_are_members(group,user_set)
        if flag:
            if len(user_set)==len(group.all_member()):
                return flag
        return False

    #判断某user是不是本组的
    def has_member(self,user):
        return self.is_member(self,user)

    #判断某一集合是否全是本组的
    def has_members(self,user_set):
        return self.all_are_members(self,user_set)

    #判断某一集合是否就是本组的全部成员
    def are_all_its_members(self,user_set):
        return self.are_all_members(self,user_set)


"""组员关系"""
class GroupMember(models.Model):
    #小组
    group = models.ForeignKey(Group)
    #组员
    user = models.ForeignKey(account.models.User)


"""好友关系"""
class Friend(models.Model):
    user = models.ForeignKey(account.models.User,related_name='user_id')
    friend = models.ForeignKey(account.models.User,related_name='friend_id')

    @classmethod
    #获取某一user的所有好友
    def all_friends(cls, user):
        lst = list(cls.objects.filter(Q(user=user)|Q(friend=user)))
        ret = []
        for item in lst:
            if(item.user.id!=user.id):
                ret.append(item.user)
                continue
            else:
                ret.append(item.firend)
        return ret

    #判断两user是否好友关系
    @classmethod
    def are_friends(cls,user1,user2):
        try:
            friend = cls.objects.get(user=user1,friend=user2)
            return True
        except:
            try:
                friend = cls.objects.get(user=user2,firend=user1)
                return True
            except:
                return False
    #成为朋友
    @classmethod
    def make_friend(cls,user1,user2):
        try:
            friend = cls(user=user1,friend=user2)
            friend.save()
        except:
            pass

"""好友请求"""
class FriendRequest(models.Model):
    from_user = models.ForeignKey(account.models.User,related_name='from_user_id')
    to_user = models.ForeignKey(account.models.User,related_name='to_user_id')
    addition_info = models.TextField()

    #确认加为好友
    def confirm(self):
        Friend.make_friend(self.from_user,self.to_user)

    #拒绝加为好友
    def refuse(self):
        self.delete()

    #获取所有请求
    @classmethod
    def find_all_request(cls,user):
        return list(cls.objects.all().filter(to_user=user))