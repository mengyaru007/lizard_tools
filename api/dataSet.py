import logging
from utils.utils import generate_fe_uuid
from api.envCon import EnvCon

class DataSet(EnvCon):

    def __init__(self, host, dataSet_name, dataSet_version = 1, name = ""):
        super().__init__(host)
        self.name = dataSet_name
        self.version = dataSet_version
        self.dataset_id = 0
        self.get_dataset_id(name)

    def get_tag_id(self, tag_name):
        """获取指定tag的id"""
        url = self.host + f"/api/v1/data-service/api/v2/datasets/{self.dataset_id}/versions/{self.version}/tags"
        res = self.session.request("get", url)
        for tag in res["result"]:
            if tag["name"] == tag_name:
                return tag["id"]

    def add_tag(self, tag_name):
        """新增tag"""
        data = {
            "name": tag_name
        }
        url = self.host + f"/api/v1/datasets/{self.dataset_id}/versions/{self.version}/tags"
        res = self.session.request("post", url, json=data)

    def get_dataset_id(self, name):
        """获取数据集版本id"""
        url = self.host + f"/api/v1/data-service/api/v2/datasets"
        params = {
            "name": name
        }
        res = self.session.request("get", url, params=params)
        for item in res['result']['list']:
            if item['name'] == self.name:
                self.dataset_id = item['id']

    def post_common_dataset(self):
        """创建公共数据集（评估用）"""
        url = self.host + f"/api/v1/data-service/api/v2/datasets"
        data = {
            "dataType": 100,
            "annotationType": 130,
            "annotationTemplateType": 131,
            "name": generate_fe_uuid(),
            "backstageFlag": 1
        }
        res = self.session.request("post", url, json=data)
        dataset_info = {
            "datasetId": res["result"]["datasetId"],
            "datasetVersionNum": res["result"]["datasetVersionNum"]
        }
        return dataset_info

    def get_published_dataset(self, name, version_name):
        """获取发布数据集（评估用）"""
        url = self.host + f"/api/v1/data-service/api/v2/dataset/published"
        params = {
            "name": name
        }
        res = self.session.request("get", url, params=params)
        dataset_info = {
            "datasetId": 0,
            "datasetVersion": 0,
            "tags": []
        }
        for item in res["result"]:
            if item["name"] == name:
                dataset_info["datasetId"] = item["id"]
                for version in item["versions"]:
                    if version_name == version:
                        dataset_info["datasetVersion"] = version["version"]
                        dataset_info["tags"] = version["tags"]
                        break
        return dataset_info

    def import_existing_common_files(self, dataset_id, dataset_version, tags):
        """上传选中测试集（评估用）"""
        dataset_info = self.post_common_dataset()
        data = {
            "datasetId": dataset_id,
            "datasetVersion": dataset_version,
            "preserveTag": True,
            "preserveAnnotation": True,
            "filterTags": tags
        }
        url = self.host + f"/api/v1/data-service/api/v2/datasets/{dataset_info['datasetId']}/versions/{dataset_info['datasetVersionNum']}/import-existing-common-files"
        res = self.session.request("post", url, json=data)
        assert res["status"] == 0, "判定节点：上传测试集失败！"

    def get_dataset_images(self):
        """获取数据集此版本下所有图片名称"""
        images = {}  # id:name
        url = self.host + f"/api/v1/data-service/api/v2/dataset/{self.dataset_id}/annotation-projects/{self.version}/samples?dataType=0&labelName=&annoFormat=lizard&pageNum=1&pageSize=99999"
        res = self.session.request("get", url)
        for item in res['result']['list']:
            images.update({item['id']: item['sampleName']})
        return images

    def get_dataset_images_info(self):
        """获取数据集此版本下所有图片信息"""
        images = {}  # id:name
        url = self.host + f"/api/v1/data-service/api/v2/dataset/{self.dataset_id}/annotation-projects/{self.version}/samples?dataType=0&labelName=&annoFormat=lizard&pageNum=1&pageSize=99999"
        res = self.session.request("get", url)
        for item in res['result']['list']:
            images.update({item['id']: item})
        return images

    def delete_images(self, image_id):
        """数据集版本中删除图片"""
        url = self.host + f"/api/v1/data-service/api/v2/dataset/{self.dataset_id}/annotation-projects/{self.version}/tasks"
        res = self.session.request("POST", url, json={"annotationIds": [image_id]})
        assert res['message'] == "成功", f"删除图片id={image_id}失败！"

    def copy_images(self, image_id, target_version):
        """同一数据集不同版本下进行复制"""
        url = self.host + f"/api/v1/data-service/api/v2/datasets/{self.dataset_id}/versions/{target_version}/import-existing-common-files"
        res = self.session.request("POST", url, json={"ids": [image_id]})
        assert res['message'] == "成功", f"复制图片id={image_id}失败！"

    def get_dataset_version_labels(self):
        """获取当前数据集版本下的labels"""
        labels = {} # name: id
        url = self.host + f"/api/v1/data-service/api/v2/datasets/{self.dataset_id}/versions/{self.version}/labels"
        res = self.session.request("get", url)
        for item in res['result']:
            labels.update({item['name']: item["id"]})
        return labels

    def add_image_label(self, image_id, data):
        """给图片标注同一修改标注类别（一张图所有的标注修改为一种类别）"""
        url = self.host +"/api/v1/datasets/actions/edit-image"
        res = self.session.request("post", url, json=data)
        assert res["status"] == 0, f"{image_id}标注失败！"

    def download_image(self, image_id, image_path, image_folder="./pictures/image.jpg"):
        """下载图片"""
        try:
            url = self.host + "/static" + image_path
            image_cont = self.session.get(url)
            with open(image_folder, 'wb') as f:
                f.write(image_cont.content)
        except Exception as e:
            logging.warning(f"下载图片image_id={image_id}失败！报错原因={e}")

    def upload_image(self, image_path, random_num):
        """上传图片"""
        url = self.host + f"/api/v1/data-service/api/v2/datasets/{self.dataset_id}/versions/{self.version}/files"
        data = {
            "random": random_num
        }
        with open(image_path, 'rb') as f:
            files = {
                'file': f
            }
            res = self.session.request("post", url, files=files, data=data)
            assert res['message'] == "成功", "数据上传图片失败！"
            return res["result"]["files"]

    def import_tasks(self,files, random_num, tags=None):
        """导入上传图片"""
        data = {
            "method": 0,
            "includingAnnotation": False,
            "annotationFormat": 0,
            "configValue": {
                "tags": tags,
                "tagMode": "merge",
                "classes": []
            },
            "creator": 1,
            "importNoAnnotationImage": True,
            "files": files,
            "random": random_num
        }
        url = self.host + f"/api/v1/datasets/{self.dataset_id}/versions/{self.version}/import-tasks"
        res = self.session.request("post", url, json=data)
        assert res['message'] == "成功", "导入上传图片失败！"

