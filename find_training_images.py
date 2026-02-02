"""查找ad节点的训练数据（原图）"""
from api.adNode import ADNode
from data.write_txt import write_txt

url = "http://10.110.156.90:9012/"
# 工程名称
model_name = "ZC-215-96H"
# 检测项名称
task_name = "cavity-front-0127"
ad_node = ADNode(url, model_name, task_name)
res = ad_node.get_ad_training_images()
original_images_name = []
images_name = []
for item in res:
    original_images_name.append(item["name"])
    prefix, suffix = item["name"].split('__NA', 1)
    # 拼接前缀 + __NA + .jpg 后缀
    new_name = f"{prefix}__NA.jpg"
    if new_name not in images_name:
        images_name.append(new_name)
write_txt(images_name, "./data/export_ng_images.txt")
print(f"原始训练数据{len(original_images_name)}张！")
print(f"原图{len(images_name)}张！")

