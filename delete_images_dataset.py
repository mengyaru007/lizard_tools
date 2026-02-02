"""
读取delete_images.txt文件，从指定数据集版本中删除
"""
import re
from api.dataSet import DataSet
from data.read_txt import read_txt

url = "http://10.110.156.90:9092/"
# 数据集名称
dataset_name = "【倍耐力增量测试-sd1inner1】sidewall1-inner1-1229--input"
# 数据集目标版本
dataset_version = "4"
# 从文件中读取的数据
dataset = DataSet(url, dataset_name, dataset_version)
dataset_version_images = dataset.get_dataset_images()
ng_images = read_txt("data/delete_images.txt")
count = 0
for key, value in dataset_version_images.items():
    # match = re.match(r'^\d+', value)
    # if match: sn = match.group()
    # else: continue
    # if sn not in ng_images:
    # 按图片名称删除或保留
    if value in ng_images:
        count += 1
        # dataSet.delete_images(key)
print(f"有{count}张重复的数据")