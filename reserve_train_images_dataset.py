"""
获取txt中加训图片数据名称，在数据集指定版本中保留这些图片，删除其余图片
1、从txt文档中按行读取要叠加的数据
2、数据集创建测试集新的版本（复制）
3、在数据集中保留读取的图片数据，删除其他
"""
from api.dataSet import DataSet
from data.read_txt import read_txt

url = "http://10.110.156.92:9006/"
# 数据集名称
dataset_name = "马牌POC-sidewall4"
# 数据集版本
dataset_version = "5"
# 从文件（add_train_images）中读取的数据
ng_images = read_txt("./data/add_train_images.txt")
# 测试集中所有图片数据
dataset = DataSet(url, dataset_name, dataset_version)
dataset_version_images = dataset.get_dataset_images()
# 仅保留文件中的图片数据，其余操作删除
for key, value in dataset_version_images.items():
    if value not in ng_images:
        dataset.delete_images(str(key))
print(f"已找到需要叠加ad数据的图片数据{len(ng_images)}张！")