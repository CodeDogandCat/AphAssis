# -*- coding: utf-8 -*-
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
reference = os.path.join(THIS_FOLDER, 'reference.py')

exec(open(reference).read())


# 训练
def doEx(request):
    setid = request.GET.get('setid')
    arrid = request.GET.get('id')
    username = request.session['username']
    userid = request.session['userid']
    classid = request.session['classid']
    print('do ex set id: ' + str(setid))
    return render(request, 'show/doEx.html',
                  {'userid': userid, 'username': username, 'classid': classid, 'arrid': arrid, 'setid': setid})


@csrf_exempt
def error_answer(request):
    error_no = request.POST.get('no', None)

    # 协同过滤需要的参数
    ques_id = questions[int(error_no) - 1].id  # 得到绝对问题id
    user_id = request.POST.get('user_id', None)
    wrong_answer = request.POST.get('wrong_choice_id', None)

    # 保存用户完整的答错题过程
    setid = request.POST.get("setid", None)
    arrid = request.POST.get("arrid", None)
    current_ques_id = request.POST.get('cur_ques_id', None)
    current_wrong_option = request.POST.get('current_wrong_option', None)

    if str(error_no) not in wrong_q:
        wrong_q.append(str(error_no))  # 用来保存顺序
    if str(error_no) not in wrong_pair:
        wrong_pair[str(error_no)] = ''  # 用来保存错题-错误选项-有效引导语  对

    right = request.POST.get('right', None)
    wrong = request.POST.get('wrong', None)
    Guider = list(guide.objects.filter(right_answer=right, wrong_answer=wrong))

    if len(Guider) > 0:
        ###算法调用
        ### 1, collab filter
        collab_tip_id = collaborative_filtering(user_id, ques_id, current_wrong_option)
        if collab_tip_id is not None:
            recom_guide_id = collab_tip_id
            # 查具体引导语信息
            result = guide.objects.get(id=recom_guide_id).tips
        else:
            ### 2, 多臂老虎机
            ### 3，random

            tip = random.sample(Guider, 1)
            print('random guide id :' + str(tip[0].id))
            recom_guide_id = tip[0].id
            result = tip[0].tips
        # 完善答错题记录
        if current_ques_id != -1:
            # 查找错题号码，追加 错选项-引导语的id
            wrong_pair[str(current_ques_id)] += str(current_wrong_option) + str('#') + str(recom_guide_id) + str('<')

        return JsonResponse({"guide": result, 'id': recom_guide_id})
    else:
        tip = ""
        # 完善答错题记录
        if current_ques_id != -1:
            # 查找错题号码，追加 错选项-引导语的id
            wrong_pair[str(current_ques_id)] += str(current_wrong_option) + str('#') + str(-1) + str('<')
        return JsonResponse({"guide": tip, 'id': -1})


# 获取指定id的套题的题目的下一道题
@csrf_exempt
def get_nextToDo(request):
    print('get next to do......')
    global number
    global questions
    global length
    global question
    global wrong_q

    user_id = request.POST.get("user_id", None)
    setid = request.POST.get("setid", None)
    arrid = request.POST.get("arrid", None)
    # 协同过滤需要保存的参数
    current_ques_id = request.POST.get('cur_ques_id', None)
    current_valid_guide_id = request.POST.get('cur_valid_guide_id', None)
    current_valid_guide_path = request.POST.get('current_valid_guide_path', None)
    current_wrong_option = request.POST.get('current_wrong_option', None)

    print("current set id : " + str(setid))
    typeid = request.POST.get("type", None)  # type==0  初始化

    if int(typeid) == 0:
        # print('get next to do......init ')
        ques_set = QuestionSet.objects.get(id=setid)
        ques_list = ques_set.questions.split(',')
        length = len(ques_list)
        for ques_id in ques_list:
            ques = Ques.objects.get(id=ques_id)
            questions.append(ques)

    current_ques_id = questions[int(current_ques_id) - 1].id  # 得到绝对问题id
    # print('get next to do......next')
    if number < length:
        question = questions[number]
        ques = str(question.question)
        imageA = str(question.imageA)
        DesA = str(question.DesA)
        imageB = str(question.imageB)
        DesB = str(question.DesB)
        imageC = str(question.imageC)
        DesC = str(question.DesC)
        imageD = str(question.imageD)
        DesD = str(question.DesD)
        voice = str(question.voice)
        # print('number : ' + str(number))
        # print('length : ' + str(length))

    # 新办法 记录每道题目的最后一个答错选项-引导语id
    if int(current_wrong_option) != -1 and len(current_valid_guide_path) != 0:
        wrong_item = wrong_record(
            userid=user_id,
            question_id=current_ques_id,
            wrong_choice=current_wrong_option,
            guide=current_valid_guide_id
        )
        wrong_item.save()

    if number < length:
        number += 1
    else:
        # print("store start")
        time_used = request.POST.get("time", None)
        w_str = ''
        # 保存全部答错题记录
        for ques_id in wrong_q:
            # print('fake ques id' + str(ques_id))
            # print('true ques id' + str(questions[int(ques_id) - 1].id))

            wrong_chice_guide_pairs = wrong_pair[ques_id]
            if wrong_chice_guide_pairs.endswith('<'):
                wrong_chice_guide_pairs = wrong_chice_guide_pairs[0:len(wrong_chice_guide_pairs) - 1]
            w_str += str(questions[int(ques_id) - 1].id) + '@' + str(wrong_chice_guide_pairs) + str(',')
        if w_str.endswith(','):
            w_str = w_str[0:len(w_str) - 1]

        arrange = Arrange_set.objects.get(id=arrid)
        arrange.usedTime = time_used
        arrange.finTime = datetime.datetime.now()
        arrange.wrong_ques = w_str
        arrange.status = 1
        arrange.save()

        number = 0
        length = 0
        questions = []
        question = None

        ques = ""
        imageA = ""
        DesA = ""
        imageB = ""
        DesB = ""
        imageC = ""
        DesC = ""
        imageD = ""
        DesD = ""
        voice = ""
    return JsonResponse({"namee": ques,
                         "imageA": imageA,
                         "DesA": DesA,
                         "imageB": imageB,
                         "DesB": DesB,
                         "imageC": imageC,
                         "DesC": DesC,
                         "imageD": imageD,
                         "DesD": DesD,
                         "voice": voice
                         })
