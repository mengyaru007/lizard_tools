from api.taskItem import TaskItem

class ClassifyNode(TaskItem):

    def __init__(self, host, model_name, task_name, node_name="分类"):
        super().__init__(host, model_name, task_name)
        self.get_node_id(node_name)

    def get_execute_result(self):
        """获取分类节点推理结果，返回[imageKey]"""
        image_keys = []
        url = self.host + f"/api/v1/projects/{str(self.project_id)}/tasks/{str(self.task_id) }/task-nodes/{str(self.node_id)}/execute-result"
        res = self.session.request("get", url)
        image_list = res['result']['list']
        for item in image_list:
            image_keys.append(item["imageKey"])
        return image_keys

    def get_classify_image_info(self, imageKey):
        """获取图片分类结果"""
        url = self.host + f"/api/v1/projects/{str(self.project_id)}/tasks/{str(self.task_id) }/task-nodes/{str(self.node_id)}/execute-result/image"
        res = self.session.request("GET", url, params={"imageKey": imageKey})
        name = res["result"]["nodeList"][0]["defects"][0]["defectName"]
        return name
