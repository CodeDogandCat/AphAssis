# -*- coding: utf-8 -*-
import os 
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
reference = os.path.join(THIS_FOLDER,'reference.py')

exec(open(reference).read())

#表情识别
# 存储用户表情识别结果
# regs = []


# 前端上传摄像头截图
@csrf_exempt
def upload_snap(request):
    if request.method == 'POST':
        # 接收图片
        snap_base64 = request.POST.get('snap_base64', None)

        # # 时间戳命名，保存图片，作为检验
        # snap = base64.b64decode(snap_base64)
        # filename = str(time.time())
        # dest = "/home/ll/dev/workspace/python/AphAssis/external/snap/" + filename + ".png"
        # if os.path.exists(dest):
        #     os.remove(dest)
        # with open(dest, "wb+") as destination:
        #     destination.write(snap)
        # print("截图保存在" + dest)
        # 分析图片，记录表情

        res = get_emotion(snap_base64)
        regs.extend(res)

        #print("表情为： ")
        #print(res)
        return JsonResponse({"face_reg_test": res[:-1]})
    # return JsonResponse({"face_reg_test": []})


# 获取表情列表
@csrf_exempt
def get_feeling(request):
    if request.method == 'POST':
        # 深拷贝
        # tmp = regs[:]
        # regs.clear()
        ##print("历史表情: ")
        ##print(tmp)
        # if len(tmp) == 0:
        #     tmp = [0]
        snap_base64 = request.POST.get('snap_base64', None)
        res = get_emotion(snap_base64)
        return JsonResponse({"feeling": res})