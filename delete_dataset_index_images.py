from api.dataSet import DataSet

url = "http://10.110.156.90:9092/"
# 数据集名称
dataset_name = "【中策AD增量对比测试】cavity-front--input"
# 数据集目标版本
dataset_version = "2"

index_min = 1
index_max = 334

score_version = ["1"]
for version in score_version:
    dataset = DataSet(url, dataset_name, version)
    dataset_version_images = dataset.get_dataset_images()
    index = 0
    for imageId, imageName in dataset_version_images.items():
        index += 1
        if index_min <= index <= index_max:
            dataset.copy_images(imageId, dataset_version)
