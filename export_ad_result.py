from api.adNode import ADNode
from data.write_txt import write_txt

url = "http://10.110.156.90:9092/"
# 工程名称
model_name = "倍耐力增量测试-sd1inner1"
# 检测项名称
task_name = "sidewall1-inner1-1229"
# 异常检测节点版本
ad_node_version = "v6.0"
# 根据ng图得分筛选
ng_min = 54.18
ng_max = 100000

ad_node = ADNode(url, model_name, task_name)
ng_images = ad_node.get_abnormal_pictures(ad_node_version, ng_min, ng_max, "异常检测")
# ng_images = ad_node.get_normal_pictures(ad_node_version, ng_min, ng_max)
write_txt(ng_images, "./data/export_ng_images.txt")