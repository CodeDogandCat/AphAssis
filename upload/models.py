# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Ques(models.Model):
	question = models.CharField(max_length=30,null=True)
	imageA = models.ImageField(upload_to='image/%Y/%m/%d/',null=True)
	DesA = models.CharField(max_length=30,null=True)
	imageB = models.ImageField(upload_to='image/%Y/%m/%d/',null=True)
	DesB = models.CharField(max_length=30,null=True)
	imageC = models.ImageField(upload_to='image/%Y/%m/%d/',null=True)
	DesC = models.CharField(max_length=30,null=True)
	imageD = models.ImageField(upload_to='image/%Y/%m/%d/',null=True)
	DesD = models.CharField(max_length=30,null=True)
	voice = models.CharField(max_length=100,null=True)
	
	def __unicode__(self):
		return self.question


class guide(models.Model):
	right_answer = models.CharField(max_length=30,null=True)
	wrong_answer = models.CharField(max_length=30,null=True)
	tips = models.CharField(max_length=60,null=True)
	def __unicode__(self):
		return self.right_answer + self.wrong_answer

class allWord(models.Model):
	word = models.CharField(max_length=30,null=True)
