"""
导出判定节点评估结果
"""
from api.decideNode import DecideNode

url = "http://10.110.156.90:9012/"
# 工程名称
model_name = "ZC-215-96H"
# 检测项名称
task_name = "cavity-front"

decide = DecideNode(url, model_name, task_name)
decide_res = decide.get_execute_result()
res = {}
for item in decide_res:
    res[item['name']] = item['evaluationResult']

sorted_res = {key: res[key] for key in sorted(res.keys())}

import csv
with open('评估结果表.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['项目名称', '评估结果'])  # 写入表头
    writer.writerows(sorted_res.items())  # 写入排序后的数据
