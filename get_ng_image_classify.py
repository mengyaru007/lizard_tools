"""
统计分类节点评估结果各个分类类别的数量
"""
from api.classifyNode import ClassifyNode

url = "http://10.110.152.15:9011/"
# 工程名称
model_name = "B94-原始分类模型"
# 检测项名称
task_name = "sidewall1-inner2-08"
res = {}
classify = ClassifyNode(url, model_name, task_name)
imageKeys = classify.get_execute_result()
for item in imageKeys:
    name = classify.get_classify_image_info(item)
    if name not in list(res.keys()):
        res[name] = 1
    else: res[name] = res[name] + 1
# 打印结果
for key, value in res.items():
    print(f"{key} = {value}")
