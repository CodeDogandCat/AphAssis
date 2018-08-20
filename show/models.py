# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.


class Recom_guide(models.Model):
    questionId = models.IntegerField(default=0)
    sentence = models.CharField(max_length=60, null=True)
    count = models.IntegerField(default=0)
    value = models.FloatField(default=0.0)
    epsilon = models.FloatField(default=0.3)
    gamma = models.FloatField(default=0.3)
    weight = models.FloatField(default=1.0)
    temperature = models.FloatField(default=0.3)
    alpha = models.FloatField(default=0.5)
    current_arm = models.IntegerField(default=0)
    next_update = models.IntegerField(default=0)
    r = models.IntegerField(default=0)


class Arrange_set(models.Model):
    userid = models.IntegerField(default=0)
    set = models.IntegerField(default=0)
    arrTime = models.DateTimeField(auto_now_add=True)
    finTime = models.DateTimeField(null=True)
    # 0 未做  1 完成
    status = models.IntegerField(default=0)
    # 如果做了的话,记录时间
    usedTime = models.FloatField(default=0.0)
    # 格式：按照答题顺序排序，
    # q@w#rg<w#rq<w#rq,
    # q@w#rg<w#rq<w#rq,
    # q@w#rg<w#rq<w#rq'，其中q指的是问题id，w是错误选项相对id，rq指的是系统提示的问题的引导语id
    wrong_ques = models.CharField(max_length=300, null=True)

class wrong_record(models.Model):
    userid=models.IntegerField(default=0)
    question_id=models.IntegerField(default=0)  # 题目在总题库里面的索引
    wrong_choice=models.IntegerField(default=0) # A,B,C,D 对应 1,2,3,4
    guide=models.IntegerField(default=0)# 引导语id

class vocab(models.Model):
    word=models.CharField(max_length=20, null=True)
