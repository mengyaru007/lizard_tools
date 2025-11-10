"""
分析判定节点评估结果
"""
import re
from lizard_class.decideNode import DecideNode

url = "http://10.110.156.90:9012/"
# 工程名称
model_name = "B94-1106"
# 检测项名称
task_name = "sidewall4-outer"

decide = DecideNode(url, model_name, task_name)
decide_res = decide.get_execute_result()
# SN:结果（有一张NG就判为NG）
res = {}
for item in decide_res:
    match = re.match(r'^\d+', item['name'])
    if match: sn = match.group()
    else: continue
    if sn not in list(res.keys()): res[sn] = item['evaluationResult']
    else:
        if not res[sn]: continue
        if res[sn] and not item['evaluationResult']: res[sn] = False

ok_nums = 0
ng_nums = 0
for key, value in res.items():
    if value: ok_nums += 1
    else:
        ng_nums += 1
        print(f"index={ng_nums} sn={key}  value={value}")
print(f"ok数量={ok_nums}，ng数量={ng_nums}")
