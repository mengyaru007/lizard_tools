from lizard_class.taskItem import TaskItem

class ADNode(TaskItem):

    def get_ad_node_config(self, node_name="异常检测"):
        """获取节点配置"""
        self.get_node_id(node_name)
        url = self.host + "/api/v1/projects/" + str(self.project_id) + "/tasks/" + str(self.task_id) + "/task-nodes/" + str(self.node_id) + "/config"
        print(f"请求接口{url}")
        res = self.session.request("get", url).json()
        print(f"{url}的响应数据：{res}")
        return res["result"]["params"]

    def get_ad_training_images(self, version = 1):
        """获取ad节点的训练数据"""
        dataset_id = self.get_ad_node_config()["datasetId"]
        url = self.host + "/api/v1/datasets/" + str(dataset_id) + "/versions/" + str(version) + "/samples"
        print(f"请求接口{url}")
        res = self.session.request("get", url).json()
        print(f"{url}的响应数据：{res}")
        return res["result"]

    def get_ad_normal_pictures(self, node_name, version, score_min, score_max):
        """获取ok图片列表"""
        self.get_ad_node_id(node_name, version)
        url = self.host + "/api/v1/projects/" + str(self.project_id) + "/tasks/" + str(self.task_id) + "/task-nodes/" + str(self.node_id) + "/execute-result?type=normal"
        print(f"请求接口{url}")
        res = self.session.request("get", url).json()
        print(f"{url}的响应数据：{res}")
        image_list = res['result']['list']
        images_name_list = []
        for imageInfo in image_list:
            if score_max >= imageInfo['score'] >= score_min:
                images_name_list.append(imageInfo['name'])
        print(f"OK图片总共{len(images_name_list)}个图片！")
        return images_name_list

    def get_ad_abnormal_pictures(self, node_name, version, score_min, score_max):
        """获取ng图片列表"""
        self.get_ad_node_id(node_name, version)
        url = self.host + "/api/v1/projects/" + str(self.project_id) + "/tasks/" + str(self.task_id) + "/task-nodes/" + str(self.node_id) + "/execute-result?type=abnormal"
        print(f"请求接口{url}")
        res = self.session.request("get", url).json()
        print(f"{url}的响应数据：{res}")
        image_list = res['result']['list']
        images_name_list = []
        for imageInfo in image_list:
            if score_max >= imageInfo['score'] >= score_min:
                images_name_list.append(imageInfo['name'])
        print(f"NG图片总共{len(images_name_list)}个图片！")
        return images_name_list