"""
分析判定节点评估结果
"""
import re
from api.decideNode import DecideNode

url = "http://10.110.156.90:9012"
# 工程名称
model_name = "ZC-215-96H"
# 检测项名称
task_name = "cavity-front"

decide = DecideNode(url, model_name, task_name)
decide_res = decide.get_execute_result()
images = {}
# SN:结果（有一张NG就判为NG）
res = {}
for item in decide_res:
    images[item['imageKey']] = item['name']
    sn = item['name'].split("__")[0]
    # match = re.match(r'^\d+', item['name'])
    # if match: sn = match.group()
    # else: continue
    if sn not in list(res.keys()): res[sn] = item['evaluationResult']
    else:
        if not res[sn]: continue
        if res[sn] and not item['evaluationResult']: res[sn] = False

ok_nums = 0
ng_nums = 0
for key, value in res.items():
    if value:
        ok_nums += 1
        print(f"index={ok_nums} sn={key}  value={value}")
    else:
        ng_nums += 1
        print(f"index={ng_nums} sn={key}  value={value}")
print(f"ok数量={ok_nums}，ng数量={ng_nums}")

# 统计ng中因某个label检出的数量
# label = "缺陷"
# label_res = 0
# label_images = []
# for item in decide_res:
#     if item['evaluationResult']: continue
#     imageKey = item['imageKey']
#     image_defects = decide.get_execute_result_image(imageKey)['defects']
#     for defect in image_defects:
#         if defect["defectName"] == label and "decision" not in defect["extra"]:
#             label_res += 1
#             label_images.append(images[imageKey])
#             break
#
# print(f"有{label}检出的图片数量={label_res}")
# print(label_images)

# # 统计ng中因异常检测+分类节点检出的数量
# ab_res = 0
# for item in decide_res:
#     if item['evaluationResult']: continue
#     imageKey = item['imageKey']
#     image_defects = decide.get_execute_result_image(imageKey)['defects']
#     for defect in image_defects:
#         if defect["score"] > float("1.00"):
#             ab_res += 1
#             break
#
# print(f"异常检测检出的图片数量={ab_res}")
#
# # 统计ng中nc的图片数量
# ab_res = 0
# for item in decide_res:
#     if item['evaluationResult']: continue
#     imageKey = item['imageKey']
#     image_defects = decide.get_execute_result_image(imageKey)['defects']
#     for defect in image_defects:
#         if defect["defectName"] == "NC":
#             ab_res += 1
#             break
#
# print(f"NC图片数量={ab_res}")
