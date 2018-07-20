#coding:utf-8
import random
import math

from upload.models import Ques
from upload.models import guide
from show.models import Recom_guide

exec(open("core.py").read())


#磊哥你好
#此处的id默认是数据库中题目的id
def getAllSentences(questionId,wrong_choice):
	needQues = list(Ques.objects.filter(id=questionId))
	guideA = list(guide.objects.filter(right_answer=needQues.question,wrong_answer=needQues.DesA))
	guideB = list(guide.objects.filter(right_answer=needQues.question,wrong_answer=needQues.DesB))
	guideC = list(guide.objects.filter(right_answer=needQues.question,wrong_answer=needQues.DesC))
	guideD = list(guide.objects.filter(right_answer=needQues.question,wrong_answer=needQues.DesD))
    if wrong_choice == 1:
        result = list(guide.objects.filter(right_answer=needQues[0].question,wrong_answer=needQues[0].DesA))
    elif wrong_choice == 2:
        result = list(guide.objects.filter(right_answer=needQues[0].question,wrong_answer=needQues[0].DesB))
    elif wrong_choice == 3:
        result = list(guide.objects.filter(right_answer=needQues[0].question,wrong_answer=needQues[0].DesC))
    elif wrong_choice == 4:
        result = list(guide.objects.filter(right_answer=needQues[0].question,wrong_answer=needQues[0].DesD))
    else 
        result = None
    return result

#磊哥你好
def getValue(questionId,sentence):
	recommand = list(Recom_guide.objects.filter(questionId=questionId,sentense=sentense))
	if len(recommand)
		t = recommand[0]
		return{"questionId":questionId,"sentence":sentence,"count":t.count,"value":t.value,"epsilon":t.epsilon,
				"gamma":t.gamma,"weight":t.weight,"temperature":t.temperature,"alpha":t.alpha,
				"current_arm":t.current_arm,"next_update":t.next_update,"r":t.r}
    #return {"count":random.randint(1,100),"value":random.random(),"epsilon":0.3,"gamma":0.3,"weight":random.random(),"temperature":0.3,"alpha":0.5,"current_arm":random.randint(1,len(getAllSentences(questionId))),"next_update":random.randint(1,len(getAllSentences(questionId))),"r":random.randint(1,len(getAllSentences(questionId)))}

def getAllAlgo():
    return ["annealing","standard","exp3","softmax_annealing","softmax_standard","ucb1","ucb2"]

#磊哥你好（这个是策略选择，可以先不急，不影响系统）
def algoSelect(userId,questionId):
    return getAllAlgo()[random.randint(0,len(getAllAlgo()))-1]

def select_arm(userId,questionId,wrong_choice):
    algo = algoSelect(userId,questionId)
    #algo = "ucb1"
    sentences = getAllSentences(questionId,wrong_choice)
    value_dict = {}
    counts_list = []
    values_list = []
    epsilon_list = []
    gamma_list = []
    weights_list = []
    temperature_list = []
    alpha_list = []
    current_arm_list = []
    next_update_list = []
    r_list = []
    for sentence in sentences:
        value_dict[sentence] = getValue(questionId,sentence)
    print (value_dict)
    print (algo)
    for sentence in sentences:
        counts_list.append(value_dict[sentence]["count"])
        values_list.append(value_dict[sentence]["value"])
        epsilon_list.append(value_dict[sentence]["epsilon"])
        gamma_list.append(value_dict[sentence]["gamma"])
        weights_list.append(value_dict[sentence]["weight"])
        temperature_list.append(value_dict[sentence]["temperature"])
        alpha_list.append(value_dict[sentence]["alpha"])
        current_arm_list.append(value_dict[sentence]["current_arm"])
        next_update_list.append(value_dict[sentence]["next_update"])
        r_list.append(value_dict[sentence]["r"])

    if algo == "annealing":
        my_algo = AnnealingEpsilonGreedy(counts = counts_list, values = values_list)
        #print my_algo.counts,my_algo.values
        chosen_arm = my_algo.select_arm()
        return {"userId":userId,"questionId":questionId,"sentences":sentences,"algo":algo,"chosen_arm":chosen_arm,"value_dict":value_dict,"my_algo":my_algo}

    if algo == "standard":
        my_algo = EpsilonGreedy(epsilon = epsilon_list[0],counts = counts_list, values = values_list)
        #print my_algo.counts,my_algo.values
        chosen_arm = my_algo.select_arm()
        return {"userId":userId,"questionId":questionId,"sentences":sentences,"algo":algo,"chosen_arm":chosen_arm,"value_dict":value_dict,"my_algo":my_algo}

    if algo == "exp3":
        my_algo = Exp3(gamma = gamma_list[0],weights = weights_list)
        #print my_algo.counts,my_algo.values
        chosen_arm = my_algo.select_arm()
        return {"userId":userId,"questionId":questionId,"sentences":sentences,"algo":algo,"chosen_arm":chosen_arm,"value_dict":value_dict,"my_algo":my_algo}

    if algo == "softmax_annealing":
        my_algo = AnnealingSoftmax(counts = counts_list, values = values_list)
        #print my_algo.counts,my_algo.values
        chosen_arm = my_algo.select_arm()
        return {"userId":userId,"questionId":questionId,"sentences":sentences,"algo":algo,"chosen_arm":chosen_arm,"value_dict":value_dict,"my_algo":my_algo}

    if algo == "softmax_standard":
        my_algo = Softmax(temperature = temperature_list[0],counts = counts_list, values = values_list)
        #print my_algo.counts,my_algo.values
        chosen_arm = my_algo.select_arm()
        return {"userId":userId,"questionId":questionId,"sentences":sentences,"algo":algo,"chosen_arm":chosen_arm,"value_dict":value_dict,"my_algo":my_algo}

    if algo == "ucb1":
        my_algo = AnnealingEpsilonGreedy(counts = counts_list, values = values_list)
        #print my_algo.counts,my_algo.values
        chosen_arm = my_algo.select_arm()
        return {"userId":userId,"questionId":questionId,"sentences":sentences,"algo":algo,"chosen_arm":chosen_arm,"value_dict":value_dict,"my_algo":my_algo}

    if algo == "ucb2":
        my_algo = UCB2(alpha = alpha_list[0], counts = counts_list, values = values_list,current_arm = current_arm_list[0],next_update = next_update_list[0], r = r_list)
        chosen_arm = my_algo.select_arm()
        value_dict[sentences[chosen_arm]]["current_arm"] = my_algo.current_arm
        value_dict[sentences[chosen_arm]]["next_update"] = my_algo.next_update
        value_dict[sentences[chosen_arm]]["r"] = my_algo.r[chosen_arm]
        return {"userId":userId,"questionId":questionId,"sentences":sentences,"algo":algo,"chosen_arm":chosen_arm,"value_dict":value_dict,"my_algo":my_algo}

#磊哥你好
def getReward(userId,questionId,sentences,algo,chosen_arm,value_dict,my_algo):
    return {"userId":userId,"questionId":questionId,"sentences":sentences,"algo":algo,"chosen_arm":chosen_arm,"value_dict":value_dict,"my_algo":my_algo,"reward":random.random()}

def update(userId,questionId,sentences,algo,chosen_arm,value_dict,my_algo,reward):
    chosen_arm = int(chosen_arm)
    value_dict[sentences[chosen_arm]]["count"]+=1
    n = value_dict[sentences[chosen_arm]]["count"]
    value = value_dict[sentences[chosen_arm]]["value"]
    new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
    value_dict[sentences[chosen_arm]]["value"] = new_value
    weights = []
    for sentence in sentences:
        weights.append(value_dict[sentence]["weight"])
    n_arms = len(weights)
    total_weight = sum(weights)
    probs = [0.0 for i in range(n_arms)]
    for arm in range(n_arms):
      probs[arm] = (1 - value_dict[sentences[chosen_arm]]['gamma']) * (weights[arm] / total_weight)
      probs[arm] = probs[arm] + (value_dict[sentences[chosen_arm]]['gamma'])*(1.0 / float(n_arms))
    
    x = reward / probs[chosen_arm]
    
    growth_factor = math.exp(((value_dict[sentences[chosen_arm]]['gamma']) / n_arms) * x)
    value_dict[sentences[chosen_arm]]["weight"] = value_dict[sentences[chosen_arm]]["weight"] * growth_factor
    return {"userId":userId,"questionId":questionId,"sentences":sentences,"algo":algo,"chosen_arm":chosen_arm,"value_dict":value_dict,"my_algo":my_algo,"reward":random.random()}
    
def updateGet(questionId,chosen_arm,value_dict,wrong_choice):
    chosen_arm = int(chosen_arm)
    sentences = getAllSentences(questionId,wrong_choice)
    sentence = sentences[chosen_arm] 
    return {"questionId":questionId,"sentence":sentence,"value": value_dict[sentence]}

#磊哥你好
def dataInsert(questionId,sentence,value,wrong_choice):
	recommand = list(Recom_guide.objects.filter(questionId=questionId,sentense=sentense))
	if len(recommand)
		recommand[0] = value
    return 0

def updateInsert(questionId,chosen_arm,value_dict,wrong_choice):
    updateValue = updateGet(questionId,chosen_arm,value_dict,wrong_choice)
    dataInsert(updateValue["questionId"],updateValue["sentence"],updateValue["value"])

    
if __name__ == "__main__":
    #print (getValue(3,'6516'))
    #print (algoSelect(15,18))
    select_dict = select_arm(15,18,1) #参数分别是userid,题目id(这里用的是题目在所有题目中的索引,从0开始),选错的选项(1,2,3,4对应A,B,C,D)
    userId = select_dict["userId"]
    questionId = select_dict["questionId"]
    sentences = select_dict["sentences"]
    algo = select_dict["algo"]
    chosen_arm = select_dict["chosen_arm"]
    value_dict = select_dict["value_dict"]
    my_algo = select_dict["my_algo"]
    reward = getReward(userId,questionId,sentences,algo,chosen_arm,value_dict,my_algo)["reward"]    
    print (update(userId,questionId,sentences,algo,chosen_arm,value_dict,my_algo,reward))
    print updateGet(questionId,chosen_arm,value_dict,1)  #这个的最后一个参数是选错的选项(1,2,3,4)

