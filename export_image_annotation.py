"""
将数据集中图片按标注切割，并保存到对应标注类别的文件夹下"./pictures"
"""
import os
from lizard_class.dataSet import DataSet
from utils.get_bounding_rect import get_bounding_rect
from utils.save_chinese_path import save_chinese_path
from utils.extract_filename import extract_filename
from utils.crop_image_by_points import crop_image_by_points

url = "http://10.110.156.90:9012/"
# 数据集名称
dataset_name = "通用分类降过杀数据"
# 数据集目标版本
dataset_version = "8"
# 记录标注结果
res = {}

dataset = DataSet(url, dataset_name, dataset_version)
dataset_version_images_info = dataset.get_dataset_images_info()
for imageId, imageInfo in dataset_version_images_info.items():
    image_name = imageInfo['sampleName']
    image_path = imageInfo["samplePath"]
    image_width = imageInfo["sampleWidth"]
    image_height = imageInfo['sampleHeight']
    annotations = imageInfo['annotationJson']
    dataset.download_image(imageId, image_path)
    name = extract_filename(image_name)
    for index in range(len(annotations)):
        label_name = annotations[index]['label']
        if label_name not in list(res.keys()):
            res[label_name] = 1
        else:
            res[label_name] = res[label_name] + 1
        coordinate = annotations[index]['box']
        points = []
        if type(coordinate) == list:
            for xy in coordinate:
                points.append((xy['x'], xy['y']))
            coordinate = get_bounding_rect(points)
        x = coordinate['x']
        y = coordinate['y']
        width = coordinate['width']
        height = coordinate['height']
        points = [(x, y), (x+width, y), (x+width, y+height), (x, y+height),]
        for i in range(len(points)):
            # 处理x坐标
            x = round(points[i][0], 3)
            x = x if x > 0 else 0
            x = x if x < image_width else image_width

            # 处理y坐标（修复判断条件）
            y = round(points[i][1], 3)
            y = y if y > 0 else 0
            y = y if y < image_height else image_height

            points[i] = (x, y)
        cropped_image = crop_image_by_points("./pictures/image.jpg", points)
        anno_name = f"{name}__{res[label_name]}.jpg"
        # 判定该类型的文件夹是否已存在
        label_dir = os.path.join("./pictures", label_name)  # label_name是中文
        os.makedirs(label_dir, exist_ok=True)
        save_chinese_path(os.path.join(label_dir, anno_name), cropped_image)

print(res)
