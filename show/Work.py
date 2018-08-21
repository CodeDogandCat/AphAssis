# -*- coding: utf-8 -*-
import os 
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
reference = os.path.join(THIS_FOLDER,'reference.py')

exec(open(reference).read())


#显示已经完成的和所有题目


# 获取已经完成的所有任务
def get_allMyDoneSet(request):
    print('get_allMyDoneSet')
    userid = request.session['userid']
    # print('current user id ": ' + str(userid))
    arrs = list(Arrange_set.objects.filter(userid=userid, status=1).order_by("-arrTime"))
    length = len(arrs)
    ans = {}
    ans["length"] = length
    for i in range(length):
        ans['id' + str(i)] = str(arrs[i].id)
        ans['setdes' + str(i)] = QuestionSet.objects.get(id=arrs[i].set).setDes
        ans["arr_set" + str(i)] = str(arrs[i].set)
        dt_arr = arrs[i].arrTime.strftime("%Y/%m/%d %H:%M:%S")
        dt_fin = arrs[i].finTime.strftime("%Y/%m/%d %H:%M:%S")
        ans["arr_datetime" + str(i)] = str(dt_arr)
        ans["fin_datetime" + str(i)] = str(dt_fin)
        ans["used_time" + str(i)] = str(arrs[i].usedTime) + '秒'
        ans["arr_userid" + str(i)] = str(arrs[i].userid)
    # toList.append(deepcopy(ans))
    return JsonResponse(ans)


# 获取要做的所有任务
def get_allMyToDoSet(request):
    print('get_allMyToDoSet')
    userid = request.session['userid']
    # print('current user id ": ' + str(userid))
    arrs = list(Arrange_set.objects.filter(userid=userid, status=0).order_by("-arrTime"))
    length = len(arrs)
    ans = {}
    ans["length"] = length
    for i in range(length):
        ans['id' + str(i)] = str(arrs[i].id)
        ans['setdes' + str(i)] = QuestionSet.objects.get(id=arrs[i].set).setDes
        ans["arr_set" + str(i)] = str(arrs[i].set)
        dt_new = arrs[i].arrTime.strftime("%Y/%m/%d %H:%M:%S")
        ans["arr_datetime" + str(i)] = str(dt_new)
        ans["arr_userid" + str(i)] = str(arrs[i].userid)
    # toList.append(deepcopy(ans))
    print(ans)
    return JsonResponse(ans)


# 显示要做的的任务
def view_allMyToDoSet(request):
    username = request.session['username']
    classid = request.session['classid']
    print('view_allMyToDoSet')
    return render(request, 'show/showMyToDoSet.html', {'username': username, 'classid': classid})


# 显示已经完成的任务
def view_allMyDoneSet(request):
    username = request.session['username']
    classid = request.session['classid']
    print('view_allMyDoneSet')
    return render(request, 'show/showMyDoneSet.html', {'username': username, 'classid': classid})
