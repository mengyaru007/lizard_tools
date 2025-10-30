"""
读取delete_images.txt文件，从指定数据集版本中删除
"""
from lizard_class.dataSet import DataSet
from data.read_txt import read_txt

url = "http://10.110.156.90:9012/"
# 数据集名称
dataset_name = "倍耐力过杀数据"
# 数据集目标版本
dataset_version = "3"
# 从文件中读取的数据
ng_images = read_txt("./data/delete_images.txt")
dataset = DataSet(url, dataset_name, dataset_version)
dataset_version_images = dataset.get_dataset_images()
for key, value in dataset_version_images.items():
    for item in ng_images:
        if item in value:
            dataset.delete_images(key)