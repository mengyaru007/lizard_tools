from lizard_class.taskItem import TaskItem

class ClassifyNode(TaskItem):

    def __init__(self, host, model_name, task_name):
        super().__init__(host, model_name, task_name)
        self.get_node_id(node_name="分类")

    def get_execute_result(self):
        """获取分类节点推理结果，返回[imageKey]"""
        image_keys = []
        url = self.host + f"/api/v1/projects/{str(self.project_id)}/tasks/{str(self.task_id) }/task-nodes/{str(self.node_id)}/execute-result"
        print(f"请求接口{url}")
        res = self.session.request("get", url).json()
        print(f"{url}的响应数据：{res}")
        image_list = res['result']['list']
        for item in image_list:
            image_keys.append(item["imageKey"])
        return image_keys

    def get_classify_image_info(self, imageKey):
        """获取图片分类结果"""
        url = self.host + f"/api/v1/projects/{str(self.project_id)}/tasks/{str(self.task_id) }/task-nodes/{str(self.node_id)}/execute-result/image"
        print(f"请求接口{url}，查看图片id={imageKey}")
        res = self.session.request("GET", url, params={"imageKey": imageKey}).json()
        name = res["result"]["nodeList"][0]["defects"][0]["defectName"]
        print(f"图片id={imageKey}的分类结果={name}")
        return name
