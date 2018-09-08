# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from upload.models import Ques
from upload.models import guide
from show.models import vocab
from login.models import register,familiarity

from aip import AipSpeech
from django.http import HttpResponse, JsonResponse
import re

APP_ID = '11055836'
API_KEY = 'lwEPvnwUvc2thvOY9G0IkqjV'
SECRET_KEY = 'GgEGZCZY9qkRP3m8b8bnTNNWcnO3N6qS'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# Create your views here.
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        ques_str = request.POST.get('question', None)
        result = client.synthesis(ques_str, 'zh', 1, {
            'vol': 5,
        })
        if not isinstance(result, dict):
            with open("media/voice/" + ques_str + '.mp3', 'wb') as f:
                f.write(result)

        words = []
        words.append(request.POST.get('desA', None))
        words.append(request.POST.get('desB', None))
        words.append(request.POST.get('desC', None))
        words.append(request.POST.get('desD', None))
        
        new_Ques = Ques(
            question=ques_str,
            imageA=request.FILES.get('imageA'),
            DesA=words[0],
            imageB=request.FILES.get('imageB'),
            DesB=words[1],
            imageC=request.FILES.get('imageC'),
            DesC=words[2],
            imageD=request.FILES.get('imageD'),
            DesD=words[3],
            voice="media/voice/" + ques_str + '.mp3'
        )
        new_Ques.save()
        ##将新出现的词汇添加到词汇表中
        addWord(words)


    username = request.session['username']
    classid = request.session['classid']
    return render(request, 'upload/uploadEx.html', {'username': username, 'classid': classid})

def addWord(words):
	print("add word:")
	print(words)
	all_user = list(register.objects.all())

	for item in words:
		if(len(vocab.objects.filter(word=item)) == 0):
			new_word = vocab(word=item)
			new_word.save()
			for user in all_user:
				new_fam = familiarity(res_id=user.id,word=item,score=50)
				new_fam.save()


#引导语的增删改查
@csrf_exempt
def guide_upload(request):
    if request.method == 'POST':
        right = request.POST.get('right', None)    #从前端的输入框里获取输入
        wrong = request.POST.get('wrong', None)
        guidance = request.POST.get('guide', None)

        guide_voice = client.synthesis(guidance, 'zh', 1, {
            'vol': 5,
        })

        if not isinstance(guide_voice, dict):
            with open("media/guide/" + guidance + ".mp3", "wb") as f:
                f.write(guide_voice)

        new_guide = guide(
            right_answer=right,
            wrong_answer=wrong,
            tips="media/guide/" + guidance + ".mp3"
        )
        new_guide.save()
    return JsonResponse({"status": 1})


# 增加引导语界面
def addGuideline(request):
    username = request.session['username']
    classid = request.session['classid']
    option_list = list(Ques.objects.all())
    ans = set()
    for item in option_list:
        if item.DesA not in ans:
            ans.add(item.DesA)
        if item.DesB not in ans:
            ans.add(item.DesB)
        if item.DesC not in ans:
            ans.add(item.DesC)
        if item.DesD not in ans:
            ans.add(item.DesD)
    res = list(ans)
    return render(request, 'addGuideline.html', {'username': username, 'classid': classid, 'options': res})


# 查询引导语界面
def viewGuideline(request):
    username = request.session['username']
    classid = request.session['classid']
    return render(request, 'viewGuideline.html', {'username': username, 'classid': classid})


# 删除引导语界面
def delGuideline(request):
    username = request.session['username']
    classid = request.session['classid']
    return render(request, 'delGuideline.html', {'username': username, 'classid': classid})


# 获取特定引导语
def get_specificGuide(request):
    right = str(request.POST.get("right", None))
    wrong = str(request.POST.get("wrong", None))

    guide_list = list(guide.objects.filter(right_answer=right, wrong_answer=wrong))
    length = len(guide_list)
    ans = {}
    ans["length"] = length
    regex = r'media/guide/(.*).mp3'

    for i in range(length):
        ans['id' + str(i)] = str(guide_list[i].id)
        ans['right' + str(i)] = str(guide_list[i].right_answer)
        ans["wrong" + str(i)] = str(guide_list[i].wrong_answer)
        ans["guide" + str(i)] = str(extractData(regex, guide_list[i].tips))
    return JsonResponse(ans)


def extractData(regex, content, index=1):
    r = '0'
    p = re.compile(regex)
    m = p.search(content)
    if m:
        r = m.group(index)
    return r


# 删除特定引导语
def submit_GuideDel(request):
    if request.method == 'POST':
        l = request.POST.get("setsCheck", None).split(',')
        for i in l:
            guideline = guide.objects.filter(id=i).delete()

    return JsonResponse({"status": 1})
