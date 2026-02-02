"""
修改数据集指定版本里所有图片的标注为指定类别
【注意】若当前数据集版本没有要添加的label，需要手动先添加
"""
from api.dataSet import DataSet

url = "http://10.110.152.15:9014/"
# 数据集名称
dataset_name = "小洞标注数据"
# 数据集目标版本
dataset_version = "1"
# 标注名称
label_name = "杂质"
dataset = DataSet(url, dataset_name, dataset_version)
dataset_id = dataset.dataset_id
# 当前数据集版本下的所有图片数据
dataset_version_images_info = dataset.get_dataset_images_info()
print(f"当前有{len(dataset_version_images_info)}张图片！")
for imageId, imageInfo in dataset_version_images_info.items():
    data = {
        "annotation": [],
        "height": imageInfo["sampleHeight"],
        "imageKey": f"{dataset_id}-{dataset_version}-{imageId}",
        "width": imageInfo["sampleWidth"]
    }
    annotations = imageInfo["annotationJson"]
    if not annotations: break
    for ann in annotations:
        ann["label"] = label_name
        ann["labels"] = [label_name]
    data["annotation"] = annotations
    dataset.add_image_label(imageId, data)