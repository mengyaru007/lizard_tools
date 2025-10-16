"""
导出整体评估中的NG图片名称
"""
from lizard_class.evaluation import Evaluation
from data.write_txt import write_txt

url = "http://10.110.152.15:9011/"
evaluation = Evaluation(url)
ng_images = list(evaluation.get_abnormal_pictures().values())
write_txt(ng_images, "./data/export_ng_images.txt")