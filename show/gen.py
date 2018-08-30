# -*- coding: utf-8 -*-
import os 
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
reference = os.path.join(THIS_FOLDER,'reference.py')

from login.models import familiarity

exec(open(reference).read())

all_sets = []
data_to_chart = []


def gen_chart(request):
    global data_to_chart
    username = request.session['username']
    classid = request.session['classid']

    return render(request, 'show/genChart.html', {'username': username, 'classid': classid})

def get_chart_data(request):
    global data_to_chart

    sets_name = ''
    wrong_count = ''
    score = ''
    time = ''
    if len(data_to_chart) > 0:
        for item in data_to_chart:  
            sets_name = sets_name +  item['name'] + ','
            wrong_count = wrong_count + str(item['count']) + ','
            score = score + str(item['count']/item['number']) + ','
            time = time + str(item['time']) + ','

    return JsonResponse({
						'name' : sets_name,
						'wrong' : wrong_count,
						'scores' : score,
						'times' : time
		})

# 显示患者的详细信息
def gen_detail(request):
    global data_to_chart

    data_to_chart.clear()

    need_gen_str = request.GET.get('id')
    need_gen_no = int(need_gen_str)
    all_sets = QuestionSet.objects.all()
    need_gen = register.objects.get(res_id=0,id=need_gen_no) # 获取患者
    print('show gen id : '+str(need_gen.id))
    sets = list(Arrange_set.objects.filter(userid=need_gen.id))  # 获取这个人对应的所有套题
    # print("len %d\n",len(sets))
    detail = []
    # 下面是患者在每套题的情况
    for item in sets:
        temp = {}
        d_chart = {}
        if item.status == 0:
            temp['status'] = '未完成'
            temp["time"] = '--'
            temp["wrong"] = '--'
            temp["fintime"] = '--'
        else:
            d_chart['time'] = item.usedTime
            temp['status'] = '已完成'
            temp["time"] = str(item.usedTime) + '秒'

            #解析错题记录
            count = 0
            w_list = str(item.wrong_ques).split(',')
            w_str = ''
            for wrong_pair in w_list:
                ls = str(wrong_pair).split('@')
                wrong_ques_id = ls[0]
                #wrong_log = ls[1]  
                w_str += str(wrong_ques_id) + ','
                count = count + 1

            if w_str.endswith(','):
                w_str = w_str[0:len(w_str) - 1]
            if len(w_str) > 10:
                w_str = w_str[0:6]
                w_str = w_str + ".."
            temp["wrong"] = w_str
            temp['fintime'] = item.finTime.strftime("%Y/%m/%d %H:%M:%S")

            all_ques = all_sets.filter(id=item.set)[0].questions

            d_chart['number'] = len(all_ques.split(','))
            d_chart['count'] = count
            d_chart['name'] = all_sets.filter(id=item.set)[0].setDes
            data_to_chart.append(d_chart)

        temp["name"] = all_sets.filter(id=item.set)[0].setDes
        temp["arrtime"] = item.arrTime.strftime("%Y/%m/%d %H:%M:%S")
        detail.append(temp)
        

    print("show gen detail len: "+str(len(detail)))
    current_page = request.GET.get('p')
    # Paginator对象，里面封装了上面那些值，把USER_LIST对象传过来了，显示10页
    paginator = Paginator(detail, 3)

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
    return render(request, 'show/genDetail.html', {'posts': posts,'genid':need_gen_no, 'username': username, 'classid': classid})


# 所有患者
def allGen(request):
    gens = list(register.objects.filter(res_id=0))
    # genList = []
    # for item in gens:
    #     temp = {}
    #     temp['id'] = i
    #     temp['name'] = item.res_username
    #     genList.append(temp)
    #     i = i + 1

    current_page = request.GET.get('p')
    # Paginator对象，里面封装了上面那些值，把USER_LIST对象传过来了，显示10页
    paginator = Paginator(gens, 3)

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
    return render(request, 'show/allGen.html', {'posts': posts, 'username': username, 'classid': classid})


def get_allGen(request):
    Gen = list(register.objects.filter(res_id=0))
    length = len(Gen)
    ans = {}
    ans["length"] = length
    for i in range(length):
        ans["gen" + str(i)] = str(Gen[i].res_username)
    # toList.append(deepcopy(ans))
    return JsonResponse(ans)


def word_fam(request):
    
    username = request.session['username']
    classid = request.session['classid']
    
    return render(request,'show/word_fam.html',{'username':username,'classid':classid})


def get_fam_data(request):
    all_user = list(register.objects.all())

    gen_list = set()
    all_fam_data = list(familiarity.objects.all())  #所有分数
    
    all_scores = {}  ##每个用户

    for user in all_user:
        s_score = list(familiarity.objects.filter(res_id=user.id))  #这个用户对应的所有的分数
        s_word = {}   ##每个用户对应的词的分数
        for item in s_score:
            s_word[item.word] = item.score

        if len(s_word) > 0:
            all_scores[user.res_username] = s_word

    '''
    all_fam = ''
    all_user = ''
    all_word = ''
    for user,words in all_scores.items():
        all_user = all_user

    for user in gen_list:
        all_user = all_user + user.res_username + ','
        for word in word_list:
            p_score = familiarity.objects.filter(res_id=user.id,word=word)
            all_fam = all_fam + str(p_score[0].score) + ','
	
    return JsonResponse({
            'users' : all_user,
            'words' : all_word,
            'scores' : all_fam
        })
	'''
    return JsonResponse(all_scores)