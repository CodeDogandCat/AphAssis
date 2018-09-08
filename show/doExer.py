# -*- coding: utf-8 -*-
import os
import show.filtering as fil
import show.hmm as _hmm

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
reference = os.path.join(THIS_FOLDER, 'reference.py')

exec(open(reference).read())

from login.models import familiarity


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
    print("do Ex wrong")
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
    ##print("before check_record")
    check_record(user_id, ques_id, right, 0)  ##都需要用绝对id
    wrong = request.POST.get('wrong', None)
    Guider = list(guide.objects.filter(right_answer=right, wrong_answer=wrong))
    print("right:" + right)
    print("wrong:" + wrong)
    
    if len(Guider) > 0:
        ##---------------现在是BKT算法的添加-------------
        answer_familiarity = list(familiarity.objects.filter(res_id=user_id, word=right))
        wrong_familiarity = list(familiarity.objects.filter(res_id=user_id, word=wrong))
        if len(wrong_familiarity) == 0 or len(answer_familiarity) == 0:
            print("Word Database Missing for user: " + str(user_id) + "!!!!")
        else:
            score_sum = answer_familiarity[0].score
            score_sum = score_sum + wrong_familiarity[0].score

            score_aver = score_sum / 200

            recom_guide_id = fil.filtering(Guider, score_aver)
            if recom_guide_id not in range(0, len(Guider)):
                tip = random.sample(Guider, 1)
                print('random guide id :' + str(tip[0].id))
                recom_guide_id = tip[0].id
                result = tip[0].tips
            else:
                result = Guider[recom_guide_id].tips
            return JsonResponse({"guide": result, 'id': recom_guide_id})
            ##-------------------------------------------
    else:
        tip = ""
        # 完善答错题记录
        if current_ques_id != -1:
            # 查找错题号码，追加 错选项-引导语的id
            wrong_pair[str(current_ques_id)] += str(current_wrong_option) + str('#') + str(-1) + str('<')
        return JsonResponse({"guide": tip, 'id': -1})


def to_bin(seq_value):
    seq_value = int(seq_value)
    seq = []
    for i in range(0, 3):
        seq.append(seq_value % 2)
        seq_value = (int)(seq_value / 2)
    seq.reverse()
    return seq


def check_record(_user_no, _ques_no, _ques_ans, score):
    global BKT_A
    global BKT_B

    record = list(answer_sequence.objects.filter(user_no=_user_no, question_no=_ques_no))

    if len(record) == 0:
        new_record = answer_sequence(
            user_no=_user_no,
            question_no=_ques_no,
            times=1,
            sequence=score
        )
        new_record.save()
    else:
        if record[0].times == 3:
            seq = []

            seq_value = record[0].sequence
            seq = to_bin(seq_value)
            print('-------------')
            print(_user_no,_ques_ans)
            words = list(familiarity.objects.filter(res_id=_user_no, word=_ques_ans))
            BKT_score = words[0].score
            BKT_score = BKT_score / 100

            BKT_Pi = [BKT_score, 1 - BKT_score]
            ##print(BKT_Pi)
            ##print(BKT_A)
            ##print(BKT_B)
            hmm = _hmm.HMM(BKT_A, BKT_B, BKT_Pi)

            return_score = hmm.baum_welch(seq)
            words[0].score = int(return_score[0] * 100)
            words[0].save()

            record[0].sequence = score
            record[0].times = 1
            record[0].save()
        else:
            record[0].sequence = record[0].sequence * 2 + score
            record[0].times = record[0].times + 1
            record[0].save()


# 做对了才会有下一道
# 序列中的1指定的是上一道题
# 获取指定id的套题的题目的下一道题
@csrf_exempt
def get_nextToDo(request):
    print('get next to do......')
    global number
    global questions
    global length
    global question
    global wrong_q
    global last_question_id
    global last_question_ans

    user_id = request.POST.get("user_id", None)

    setid = request.POST.get("setid", None)
    arrid = request.POST.get("arrid", None)

    # 协同过滤需要保存的参数
    current_ques_id = request.POST.get('cur_ques_id', None)
    realitive_ques_id = current_ques_id

    if int(current_ques_id) == -1:
        current_ques_id = 1
    print("current_question_id: " + str(current_ques_id))

    current_valid_guide_id = request.POST.get('cur_valid_guide_id', None)
    current_valid_guide_path = request.POST.get('current_valid_guide_path', None)
    current_wrong_option = request.POST.get('current_wrong_option', None)

    print("current set id : " + str(setid))
    typeid = request.POST.get("type", None)  # type==0  初始化

    if int(typeid) == 0:
        print('get next to do......init ')
        ques_set = QuestionSet.objects.get(id=setid)
        ques_list = ques_set.questions.split(',')
        length = len(ques_list)
        for ques_id in ques_list:
            ques = Ques.objects.get(id=ques_id)
            questions.append(ques)  ##questions是全局变量

    if last_question_id != -1:
        last_question_id = questions[int(current_ques_id) - 1].id
        last_question_ans = questions[int(current_ques_id) - 1].question
        current_ques_id = questions[int(current_ques_id) - 1].id  # 得到绝对问题id
        check_record(user_id, last_question_id, last_question_ans, 1)
    else:  ##第一次调用获得第一道题
        tmp = current_ques_id
        print("$$$$$$$$" + str(tmp))
        current_ques_id = questions[int(current_ques_id) - 1].id  # 得到绝对问题id
        last_question_id = current_ques_id
        
        print("show_id:" + str(current_ques_id))
        print("show len:" + str(len(questions)))
        print("curr_ques_id:",int(current_ques_id))
        last_question_ans = questions[int(realitive_ques_id) - 1].question

    # 现在假定这里的就是绝对id(数据库里面每一项自带一个id,现在说的就是那个)
    # 也假定现在的user_id同上
    # 这里重新写一个函数,对数据库操作

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
