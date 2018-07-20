# -*- coding: utf-8 -*-
import os 
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
reference = os.path.join(THIS_FOLDER,'reference.py')
expre = os.path.join(THIS_FOLDER,'expre.py')

exec(open(reference).read())
exec(open(expre).read())


def index(request):
    username = request.session['username']
    classid = request.session['classid']
    userid = request.session['userid']
    return render(request, 'show/index.html',
                  {'userid': userid, 'username': username, 'classid': classid})


# 显示全部题目
def showAllEx(request):
    all_ques = Ques.objects.all()
    questions = list(all_ques)
    for ques in questions:
        ques.imageA = '/media/' + ques.imageA.__str__()
        ques.imageB = '/media/' + ques.imageB.__str__()
        ques.imageC = '/media/' + ques.imageC.__str__()
        ques.imageD = '/media/' + ques.imageD.__str__()
    count = all_ques.count()
    # 使用分页组件  分页显示
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    # 全部数据:USER_LIST,=>得出共有多少条数据
    # per_page: 每页显示条目数量
    # count:    数据总个数
    # num_pages:总页数
    # page_range:总页数的索引范围，如: (1,10),(1,200)
    # page:     page对象 (是否具有下一页，是否有上一页)

    current_page = request.GET.get('p')
    # Paginator对象，里面封装了上面那些值，把USER_LIST对象传过来了，显示10页
    paginator = Paginator(questions, 3)
    try:
        # page对象
        # posts配置对象(current_page用户可能填些不合法的字段）
        # paginator通过拿到了page对象，把current_page传进来
        posts = paginator.page(current_page)
        # has_next              是否有下一页
        # next_page_number      下一页页码
        # has_previous          是否有上一页
        # previous_page_number  上一页页码
        # object_list           分页之后的数据列表,已经切片好的数据
        # number                当前页
        # paginator             paginator对象

    # 表示你填的东西不是个整数
    except PageNotAnInteger:
        posts = paginator.page(1)
    # 空页的时候，表示你看完了，显示最后一页
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    username = request.session['username']
    classid = request.session['classid']

    return render(request, 'show/showAllEx.html', {'posts': posts, 'username': username, 'classid': classid})




@csrf_exempt
def submit_arr(request):
    l = request.POST.get("setsCheck", None).split(',')
    patientid = request.POST.get("userid", None)
    # print(patientid)

    for i in l:
        new_arr = Arrange_set(
            userid=int(patientid),
            set=i
        )
        new_arr.save()

    return JsonResponse({"status": 1})
