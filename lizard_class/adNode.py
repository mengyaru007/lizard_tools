from lizard_class.taskItem import TaskItem

class ADNode(TaskItem):

    def get_normal_pictures(self, version, score_min, score_max):
        """获取ok图片列表"""
        self.get_node_id(version)
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

    def get_abnormal_pictures(self, version, score_min, score_max):
        """获取ng图片列表"""
        self.get_node_id(version)
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