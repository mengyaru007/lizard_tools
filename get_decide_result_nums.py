"""
分析判定节点评估结果
"""
from api.decideNode import DecideNode

url = "http://10.110.156.90:9012"
# 工程名称
model_name = "通用X光-有监督模型"
# 检测项名称
task_name = "胎面下气泡检测"

decide = DecideNode(url, model_name, task_name)
decide_res = decide.get_execute_result()
ok_num = 0
ng_num = 0

for item in decide_res:
    if item['evaluationResult'] is True:
        ok_num += 1
    else: ng_num += 1
print(f"ok_num={ok_num};ng_num={ng_num}")