多臂老虎机：

重点：test_aphasia.py（其他的学长统统不要管）

准备工作：首先数据库中建立一张参数表：学长完成23333

(questionId,sentence,count,value,epsilon,gamma,weight,temperature,alpha,current_arm,next_update,r)

对每一个问题下辖的每一个引导语，在该表中插入一行对应数据

questionId:问题id，整形
sentence:questionId对应的问题的某一句引导语，字符串
count:整形，初值为0
value：浮点数，初值为0.0
epsilon：浮点数，初值建议0.3
gamma：浮点数，初值建议0.3
weight:浮点数，初值为1.0
temperature：浮点数，初值建议0.3
alpha：浮点数，初值建议0.5
current_arm：整形，初值为0
next_update：整形，初值为0
r：整形，初值为0

（所有“初值建议”的参数均为0到1之间可调参数，建议为0.3的不宜过大）



test_aphasia.py各函数解读：


getAllSentences(questionId)：学长完成23333
得到questionId对应问题的所有引导语，按固定顺序的列表，学长完成23333


getValue(questionId,sentence)：学长完成23333
得到questionId下辖的引导语对应的所有参数（即questionId,sentence,count,value,epsilon,gamma,weight,temperature,alpha,current_arm,next_update,r），用如{"count":random.randint(1,100),"value":random.random(),"epsilon":0.3,"gamma":0.3,"weight":random.random(),"temperature":0.3,"alpha":0.5,"current_arm":random.randint(1,len(getAllSentences(questionId))),"next_update":random.randint(1,len(getAllSentences(questionId))),"r":random.randint(1,len(getAllSentences(questionId)))}这种形式的字典存储，学长完成23333


getAllAlgo()：
多臂老虎机目前一共有七种策略，分别为"annealing","standard","exp3","softmax_annealing","softmax_standard","ucb1","ucb2"，该函数仅为获取七种算法的名字


algoSelect(userId,questionId)：
对于用户userId和题目questionId，进行多臂老虎机策略的选择，目前为随机，今后可作为强化学习的应用场景


select_arm(userId,questionId)：
对于用户userId和题目questionId，返回字典{"userId":userId,"questionId":questionId,"sentences":sentences（引导语列表）,"algo":algo（算法名）,"chosen_arm":chosen_arm（被选引导语在引导语列表sentences中下标）,"value_dict":value_dict（二维字典，第一维为sentence，第二维为该sentence对应的参数表）,"my_algo":my_algo（各策略以类的形式实现，my_algo是策略类的实例对象）}


getReward(userId,questionId,sentences,algo,chosen_arm,value_dict,my_algo)：
用户userId，题目questionId，引导语列表sentences，所选策略algo，引导语相关参数value_dict，被选句子下标chosen_arm，策略类my_algo，返回值为select_arm(userId,questionId)函数返回的字典形式，加一项"reward":表示此次多臂老虎机选择所获收益（建议以患者答题正确与否和患者答题所花时间长短为依据进行计算，比如最简单的二者相除，希望别超过1），最终形式为
{"userId":userId,"questionId":questionId,"sentences":sentences,"algo":algo,"chosen_arm":chosen_arm,"value_dict":value_dict,"my_algo":my_algo,"reward":random.random()}


update(userId,questionId,sentences,algo,chosen_arm,value_dict,my_algo,reward):
用户userId，题目questionId，引导语列表sentences，所选策略algo，引导语相关参数value_dict，被选句子下标chosen_arm，策略类my_algo，收益值reward。
目的：更新被选引导语的参数表中值，返回值形式和getReward函数形式相同，仅仅是value_dict中所保存的参数有变


updateGet(questionId,chosen_arm,value_dict):
questionId中对应的第chosen_arm条引导语被选，该函数返回该被选引导语对应的参数表


dataInsert(questionId,sentence,value):学长完成23333
题目questionId，引导语sentence，对应新的参数字典value(形式同getValue函数返回值)，在数据库对应位置将其更新，学长完成23333


updateInsert(questionId,chosen_arm,value_dict):返回该被选引导语对应的参数表，在数据库对应位置将其更新




系统流程总结：

1 当患者做题出错时，调用select_arm(userId,questionId)，保存其返回的字典，并将返回字典中的引导语列表sentences中的第chosen_arm项对应引导语显示给患者。其中userId表示用户，questionId表示出错题目id。

2 患者拿到引导语之后，会二次做题。当患者二次作答完毕，reward也就随之产生，将其加入第1步返回的字典中（以"reward":的形式），得到新字典

3 得到新字典之后，调用update(userId,questionId,sentences,algo,chosen_arm,value_dict,my_algo,reward)，其中所需各参数从第2步中得到的新字典获取。该函数执行完毕之后会返回新字典，保存

4 调用updateInsert(questionId,chosen_arm,value_dict)，其中各参数取自第3步得到的新字典。


学长任务：
1 按照我说的先建立数据库
2 根据数据库系统和答题系统完成未完成的函数
