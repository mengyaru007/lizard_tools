"""
根据ad评估结果在数据集中筛选叠加ad训练数据
1、ad节点评估
2、数据集创建测试集
3、在数据集中仅保留ng过杀的数据
"""
from api.adNode import ADNode
from api.dataSet import DataSet

url = "http://10.110.156.90:9012/"
# 工程名称
model_name = "ZC-215-96H"
# 检测项名称
task_name = "cavity-front-0127"
# 异常检测节点版本
ad_node_version = "v1.0"
# 数据集名称
dataset_name = "ZC-西湖-215"
# 数据集版本
dataset_version = "4"
# 根据ng图得分筛选
ng_min = 45
ng_max = 1000

ad_node = ADNode(url, model_name, task_name)
dataset = DataSet(url, dataset_name, dataset_version)
ng_images = ad_node.get_abnormal_pictures(ad_node_version, ng_min, ng_max)
dataset_version_images = dataset.get_dataset_images()
for key, value in dataset_version_images.items():
    if value in ng_images:
        dataset.delete_images(str(key))
print(f"已找到需要叠加ad数据的图片数据{len(ng_images)}张！")