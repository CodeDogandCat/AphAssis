# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import random
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from upload.models import Ques, guide
from show.models import Arrange_set
from makeSet.models import QuestionSet
from login.models import register
from django.http import HttpResponse, JsonResponse
import datetime, time
# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from show.models import wrong_record
from show.Collaborative_filtering.sim import  collaborative_filtering

import datetime
import time
import os
import base64
from face.run import get_emotion
from show.models import Recom_guide


number = int(0)
questions = []
length = 0
question = None
wrong_q = []
wrong_pair = {}