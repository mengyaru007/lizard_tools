"""
同一数据集下从不同版本中复制NG图片
"""
from lizard_class.dataSet import DataSet
from data.read_txt import read_txt

url = "http://10.110.156.90:9012/"
# 数据集名称
dataset_name = "倍耐力过杀数据"
# 数据集目标版本
dataset_target_version = "7"
# 从文件中读取的数据
ng_images = read_txt("./data/export_ng_images.txt")
# 来源版本
score_version = ["6"]
for version in score_version:
    dataset = DataSet(url, dataset_name, version)
    dataset_version_images = dataset.get_dataset_images()
    for value in ng_images:
        for imageId, imageName in dataset_version_images.items():
            if value == imageName:
                dataset.copy_images(imageId, dataset_target_version)