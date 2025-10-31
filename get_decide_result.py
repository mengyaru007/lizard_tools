"""
分析判定节点评估结果
"""
import re
from lizard_class.decideNode import DecideNode

url = "http://10.110.156.90:9012/"
# 工程名称
model_name = "B94-胎里正面"
# 检测项名称
task_name = "cavity-front"

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

for key, value in res.items():
    print(f"sn={key}  value={value}")
