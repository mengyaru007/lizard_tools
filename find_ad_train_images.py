"""
根据ad评估结果在数据集中筛选叠加ad训练数据
1、ad节点评估
2、数据集创建测试集
3、在数据集中仅保留ng过杀的数据
"""
from lizard_class.adNode import ADNode
from lizard_class.dataSet import DataSet

url = "http://10.110.152.15:9009/"
# 工程名称
model_name = "B94"
# 检测项名称
task_name = "sidewall2-outer"
# 异常检测节点版本
ad_node_version = "v1.0"
# 数据集名称
dataset_name = "倍耐力-0918数据"
# 数据集版本
dataset_version = "6"
# 根据ng图得分筛选
ng_min = 1
ng_max = 49

ad_node = ADNode(url, model_name, task_name)
dataset = DataSet(url, dataset_name, dataset_version)
ng_images = ad_node.get_abnormal_pictures(ad_node_version, ng_min, ng_max)
dataset_version_images = dataset.get_dataset_images()
for key, value in dataset_version_images.items():
    if value not in ng_images:
        dataset.delete_images(str(key))
print(f"已找到需要叠加ad数据的图片数据{len(ng_images)}张！")