import logging

from lizard_class.envCon import EnvCon

class DataSet(EnvCon):

    def __init__(self, host, dataSet_name, dataSet_version = 1):
        super().__init__(host)
        self.name = dataSet_name
        self.version = dataSet_version
        self.dataset_id = 0
        self.get_dataset_id()

    def get_dataset_id(self):
        """获取数据集版本id"""
        url = self.host + "/api/v1/data-service/api/v2/datasets"
        print(f"请求接口{url}")
        res = self.session.request("get", url).json()
        print(f"{url}的响应数据：{res}")
        for item in res['result']['list']:
            if item['name'] == self.name:
                self.dataset_id = item['id']

    def get_dataset_images(self):
        """获取数据集此版本下所有图片名称"""
        images = {}  # id:name
        url = self.host + f"/api/v1/data-service/api/v2/dataset/{self.dataset_id}/annotation-projects/{self.version}/samples?dataType=0&labelName=&annoFormat=lizard&pageNum=1&pageSize=99999"
        print(f"请求接口{url}")
        res = self.session.request("get", url).json()
        for item in res['result']['list']:
            images.update({item['id']: item['sampleName']})
        return images

    def get_dataset_images_info(self):
        """获取数据集此版本下所有图片信息"""
        images = {}  # id:name
        url = self.host + f"/api/v1/data-service/api/v2/dataset/{self.dataset_id}/annotation-projects/{self.version}/samples?dataType=0&labelName=&annoFormat=lizard&pageNum=1&pageSize=99999"
        print(f"请求接口{url}")
        res = self.session.request("get", url).json()
        print(f"{url}的响应数据：{res}")
        for item in res['result']['list']:
            images.update({item['id']: item})
        return images

    def delete_images(self, image_id):
        """数据集版本中删除图片"""
        url = self.host + f"/api/v1/data-service/api/v2/dataset/{self.dataset_id}/annotation-projects/{self.version}/tasks"
        print(f"请求接口{url}，删除的图片id={image_id}")
        res = self.session.request("POST", url, json={"annotationIds": [image_id]}).json()
        print(f"{url}的响应数据：{res}")
        assert res['message'] == "成功", f"删除图片id={image_id}失败！"

    def copy_images(self, image_id, target_version):
        """同一数据集不同版本下进行复制"""
        url = self.host + f"/api/v1/data-service/api/v2/datasets/{self.dataset_id}/versions/{target_version}/import-existing-common-files"
        print(f"请求接口{url}，复制的图片id={image_id}，复制到的版本={target_version}")
        res = self.session.request("POST", url, json={"ids": [image_id]}).json()
        print(f"{url}的响应数据：{res}")
        assert res['message'] == "成功", f"复制图片id={image_id}失败！"

    def get_dataset_version_labels(self):
        """获取当前数据集版本下的labels"""
        labels = {} # name: id
        url = self.host + f"/api/v1/data-service/api/v2/datasets/{self.dataset_id}/versions/{self.version}/labels"
        print(f"请求接口{url}")
        res = self.session.request("get", url).json()
        for item in res['result']:
            labels.update({item['name']: item["id"]})
        return labels

    def add_image_label(self, image_id, data):
        """给图片标注同一修改标注类别（一张图所有的标注修改为一种类别）"""
        url = self.host +"/api/v1/datasets/actions/edit-image"
        print(f"请求接口{url}，修改标注的图片id={image_id}，标注信息={data}")
        res = self.session.request("post", url, json=data).json()
        assert res["status"] == 0, f"{image_id}标注失败！"
        print(f"标注图片{image_id}成功！")

    def download_image(self, image_id, image_path, image_folder="./pictures/image.jpg"):
        """下载图片"""
        try:
            url = self.host + "/static" + image_path
            image_cont = self.session.get(url)
            with open(image_folder, 'wb') as f:
                f.write(image_cont.content)
        except Exception as e:
            logging.warning(f"下载图片image_id={image_id}失败！报错原因={e}")

