"""数据集上传大量图片"""
from biz.dataSet.upload_images import upload_images

file_path = "./pictures"
host = "http://10.110.156.90:9012/"
dataset_name = "ZC-215-96H-胎里正面-测试数据"
version = "10"
tag = "0128"
upload_images(host, dataset_name, version, tag,file_path)