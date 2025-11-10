"""
读取delete_images.txt文件，从指定数据集版本中删除
"""
import re
from lizard_class.dataSet import DataSet
from data.read_txt import read_txt

url = "http://10.110.156.90:9012/"
# 数据集名称
dataset_name = "倍耐力过杀数据1031"
# 数据集目标版本
dataset_version = "15"
# 从文件中读取的数据
ng_images = read_txt("./data/delete_images.txt")
dataset = DataSet(url, dataset_name, dataset_version)
dataset_version_images = dataset.get_dataset_images()
for key, value in dataset_version_images.items():
    match = re.match(r'^\d+', value)
    if match: sn = match.group()
    else: continue
    if sn not in ng_images:
        dataset.delete_images(key)