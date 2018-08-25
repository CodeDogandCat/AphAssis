# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import random
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from upload.models import Ques, guide
from show.models import Arrange_set
from show.models import answer_sequence
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
from show.hmm import HMM
from show.hmm import matrix

number = int(0)
questions = []
length = 0
question = None
wrong_q = []
wrong_pair = {}
last_question_id = int(-1)
last_question_ans = ''

BKT_A = {"掌握该词":{"掌握该词":0.7,"未掌握该词":0.3},"未掌握该词":{"掌握该词":0.25,"未掌握该词":0.75}}  	
BKT_B = {"掌握该词":{"答对":0.6,"答错":0.4},"未掌握该词":{"答对":0.25,"答错":0.75}}
status = ["掌握该词","未掌握该词"]
observations = ["答对","答错"]

BKT_A = matrix(BKT_A,status,status)
BKT_B = matrix(BKT_B,status,observations)
