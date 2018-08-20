# -*- coding: utf-8 -*-
import os 
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
reference = os.path.join(THIS_FOLDER,'reference.py')

exec(open(reference).read())


# 套题的分配
def setArrange(request):
    # 获取全部的患者
    patients = list(register.objects.filter(res_id=0))
    username = request.session['username']
    classid = request.session['classid']
    return render(request, 'show/setArrange.html',
                  {'username': username, 'classid': classid, 'patients': patients})


# 所有套题
def setDisplay(request):
    sets = list(QuestionSet.objects.all())
    setlist = []

    for item in sets:
        tmp = {}
        tmp['id'] = item.id
        tmp['setDes'] = item.setDes
        tmp['count'] = len(str(item.questions).split(','))
        tmp['questions'] = str(item.questions).split(',')
        tmp['href'] = '/set_detail?id=' + str(item.id)
        setlist.append(tmp)
    # 使用分页组件  分页显示

    # 全部数据:USER_LIST,=>得出共有多少条数据
    # per_page: 每页显示条目数量
    # count:    数据总个数
    # num_pages:总页数
    # page_range:总页数的索引范围，如: (1,10),(1,200)
    # page:     page对象 (是否具有下一页，是否有上一页)

    current_page = request.GET.get('p')
    # Paginator对象，里面封装了上面那些值，把USER_LIST对象传过来了，显示10页
    paginator = Paginator(setlist, 3)
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
    return render(request, 'show/showAllSet.html', {'posts': posts, 'username': username, 'classid': classid})


# 获取全部的套题
def get_allSets(request):
    sets = list(QuestionSet.objects.all())

    ans = {}
    ans['length'] = len(sets)

    for i in range(ans['length']):
        ans["id" + str(i)] = str(sets[i].id)
        ans["setDes" + str(i)] = str(sets[i].setDes)
        ans["count" + str(i)] = str(len(str(sets[i].questions).split(',')))
        ans["questions" + str(i)] = str(sets[i].questions)
    print("get all sets")
    print(ans)

    return JsonResponse(ans)



# 显示套题详情
def set_detail(request):
    if request.method == 'GET':
        id = request.GET.get('id', None)
        m = QuestionSet.objects.get(id=id)
        if m:
            questions = list()
            questions_id = m.questions.split(',')
            for quesid in questions_id:
                ques = Ques.objects.get(id=quesid)
                ques.imageA = '/media/' + ques.imageA.__str__()
                ques.imageB = '/media/' + ques.imageB.__str__()
                ques.imageC = '/media/' + ques.imageC.__str__()
                ques.imageD = '/media/' + ques.imageD.__str__()
                questions.append(ques)

            count = len(questions)
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

            return render(request, 'show/showSetDetail.html',
                          {'posts': posts, 'username': username, 'classid': classid, 'setid': id})
        else:
            return render(request, 'login/login.html')