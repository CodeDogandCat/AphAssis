from __future__ import unicode_literals

import json

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from login.models import register
from upload.models import guide

user_id = -1
Login_user = ''


def logout(request):
    if request.session.has_key('userid'):
        del request.session['userid']
    if request.session.has_key('username'):
        del request.session['username']
    if request.session.has_key('classid'):
        del request.session['classid']
    return render(request, 'login/login.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        m = register.objects.filter(res_username=username, res_password=password)
        if m:
            request.session['userid'] = m[0].id
            request.session['username'] = username
            request.session['classid'] = m[0].res_id
            print('classid' + str(m[0].res_id))
            resp = {'status': 'success', 'reason': '登录成功'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            user_id = -1
            resp = {'status': 'failed', 'reason': '用户名或密码错误'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
    return render(request, 'login/login.html')


def nregister(request):
    if request.method == 'POST':
        res_username = request.POST.get('res_username', None)
        res_password = request.POST.get('res_password', None)
        res_email = request.POST.get('res_email', None)
        res_id = request.POST.get('res_type', None)
        age = request.POST.get('age', None)
        profession = request.POST.get('profession', None)
        education = request.POST.get('education', None)
        a = register.objects.filter(Q(res_username=res_username))
        flag = 0
        for e in a:
            flag = 1
            break
        if (flag == 1):
            resp = {'status': 'failed', 'reason': '用户名重复'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            new_register = register(
                res_username=res_username,
                res_password=res_password,
                res_email=res_email,
                res_id=res_id,
                age=age,
                profession=profession,
                education=education
            )
            new_register.save()
            resp = {'status': 'success', 'reason': '注册成功'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
    return render(request, 'login/register.html')


# 设置语音页面
def viewSetSound(request):
    username = request.session['username']
    classid = request.session['classid']
    # 获取用户的设置
    cur_setting = "郭德纲"
    # 获取可能的选择
    # option_list = list(Ques.objects.all())
    ans = set()
    ans.add("习近平")
    ans.add("单田芳")
    ans.add("赵本山")
    ans.add("郭德纲")
    ans.add("林志玲")
    res = list(ans)
    return render(request, 'login/setSound.html',
                  {'username': username, 'classid': classid, 'cur_sound_name': cur_setting, 'options': res})


# 设置语音偏好
def saveSoundSetting(request):
    if request.method == 'POST':
        sound_name = request.POST.get('sound_name', None)  # 从前端的输入框里获取输入

        # 更新数据库
        print("更新数据库" + str(sound_name))

        ####
    return JsonResponse({"status": 1})


# 生成语音
def getSound(request):
    test_text = ""
    if request.method == 'POST':
        test_text = request.POST.get('test_text', None)  # 从前端的输入框里获取输入

        print("生成语音" + str(test_text))

    return JsonResponse({"sound": str(test_text), "status": 1})
