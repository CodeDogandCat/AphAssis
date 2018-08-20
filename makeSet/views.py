# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import random
from copy import deepcopy
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from upload.models import Ques, guide
from django.http import HttpResponse, JsonResponse
from makeSet.models import QuestionSet
# Create your views here.

#制作套题
def makeSet(request):
    username = request.session['username']
    classid = request.session['classid']
    return render(request, 'makeSet/makeSet.html', {'username': username, 'classid': classid})


@csrf_exempt
def get_all_set(request):
    questions = list(Ques.objects.all())
    length = len(questions)
    # toList = []
    # toList.append(length)
    ans = {}
    ans["length"] = length
    for i in range(length):
        ans["id" + str(i)] = str(questions[i].id)
        ans["ques" + str(i)] = str(questions[i].question)
        ans["imageA" + str(i)] = str(questions[i].imageA)
        ans["DesA" + str(i)] = str(questions[i].DesA)
        ans["imageB" + str(i)] = str(questions[i].imageB)
        ans["DesB" + str(i)] = str(questions[i].DesB)
        ans["imageC" + str(i)] = str(questions[i].imageC)
        ans["DesC" + str(i)] = str(questions[i].DesC)
        ans["imageD" + str(i)] = str(questions[i].imageD)
        ans["DesD" + str(i)] = str(questions[i].DesD)
        ans["voice" + str(i)] = str(questions[i].voice)
    # toList.append(deepcopy(ans))
    print(ans)

    return JsonResponse(ans)


@csrf_exempt
def submit_set(request):
    # l = request.POST.get("quesCheck", None).split(',')
    des = request.POST.get("setDes", None)
    # ans = []
    # for i in range(len(l)):
    #     if l[i] == "true":
    #         ans.append(i)
    # ans_string = str(ans[0])
    # for i in range(len(ans)):
    #     if i == 0:
    #         continue
    #     ans_string = ans_string + ","
    #     ans_string = ans_string + str(ans[i])
    t = list(QuestionSet.objects.all())
    now_id = 0
    if len(t) > 0:
        now_id = t[len(t) - 1].setId + 1
    new_set = QuestionSet(
        setId=now_id,
        questions=request.POST.get("quesCheck", None),
        setDes=des)

    new_set.save()
    return JsonResponse({"status": 1})
