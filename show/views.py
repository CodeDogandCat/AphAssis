# -*- coding: utf-8 -*-
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
reference = os.path.join(THIS_FOLDER, 'reference.py')
expre = os.path.join(THIS_FOLDER, 'expre.py')

exec(open(reference).read())
exec(open(expre).read())
from login.models import register


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
    paginator = Paginator(questions, 8)
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


def get_patient_account(request):
    username = request.session['username']
    classid = request.session['classid']
    patientid = request.GET.get("id", None)
    print("patientid " + str(patientid))
    patient = register.objects.get(id=int(patientid))
    res_username = "" if patient.res_username is None else patient.res_username
    res_password = "" if patient.res_password is None else patient.res_password
    res_email = "" if patient.res_email is None else patient.res_email
    age = "" if patient.age is None else patient.age
    profession = "" if patient.profession is None else patient.profession
    education = "" if patient.education is None else patient.education
    training_start_period = "" if patient.training_start_period is None else patient.training_start_period.strftime(
        '%Y-%m-%d')
    print("##########")
    print(type(training_start_period))
    severe = "" if patient.severe is None else patient.severe
    comorbidity_disease = "" if patient.comorbidity_disease is None else patient.comorbidity_disease
    primary_disease = "" if patient.primary_disease is None else patient.primary_disease
    type_of_aphasia = "" if patient.type_of_aphasia is None else patient.type_of_aphasia
    personality = "" if patient.personality is None else patient.personality
    intelligence = "" if patient.intelligence is None else patient.intelligence
    language_background = "" if patient.language_background is None else patient.language_background
    self_correcting_ability = "" if patient.self_correcting_ability is None else patient.self_correcting_ability
    sound = "默认" if patient.selected_speech is None else patient.selected_speech
    # toList.append(deepcopy(ans))
    return render(request, 'show/patientArchives.html', {'res_username': res_username,
                                                         'res_password': res_password,
                                                         'res_email': res_email,
                                                         'age': age,
                                                         'profession': profession,
                                                         'education': education,
                                                         'training_start_period': training_start_period,
                                                         'severe': severe,
                                                         'comorbidity_disease': comorbidity_disease,
                                                         'primary_disease': primary_disease,
                                                         'type_of_aphasia': type_of_aphasia,
                                                         'personality': personality,
                                                         'intelligence': intelligence,
                                                         'language_background': language_background,
                                                         'self_correcting_ability': self_correcting_ability,
                                                         'sound': sound,
                                                         'username': username, 'classid': classid})


def save_patient_account(request):
    if request.method == 'POST':
        res_username = request.POST.get('res_username', None)
        res_password = request.POST.get('res_password', None)
        res_email = request.POST.get('res_email', None)
        age = request.POST.get('age', None)
        profession = request.POST.get('profession', None)
        education = request.POST.get('education', None)
        training_start_period = request.POST.get('training_start_period', None)
        severe = request.POST.get('severe', None)
        comorbidity_disease = request.POST.get('comorbidity_disease', None)
        primary_disease = request.POST.get('primary_disease', None)
        type_of_aphasia = request.POST.get('type_of_aphasia', None)
        personality = request.POST.get('personality', None)
        intelligence = request.POST.get('intelligence', None)
        language_background = request.POST.get('language_background', None)
        self_correcting_ability = request.POST.get('self_correcting_ability', None)
        sound = request.POST.get('sound', '默认')
        patient = register.objects.get(res_username=res_username)
        if patient.res_password != res_password:
            patient.res_password = res_password
        patient.res_username = res_username
        patient.res_email = res_email
        patient.res_id = 0
        patient.age = age
        patient.profession = profession
        patient.education = education
        patient.training_start_period = training_start_period
        patient.severe = severe
        patient.comorbidity_disease = comorbidity_disease
        patient.primary_disease = primary_disease
        patient.type_of_aphasia = type_of_aphasia
        patient.personality = personality
        patient.intelligence = intelligence
        patient.language_background = language_background
        patient.self_correcting_ability = self_correcting_ability
        patient.selected_speech = sound

        patient.save()
        resp = {'status': 'success', 'reason': '保存成功'}
        return HttpResponse(json.dumps(resp), content_type="application/json")
