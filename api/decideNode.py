from api.taskItem import TaskItem

class DecideNode(TaskItem):

    def __init__(self, host, model_name, task_name):
        super().__init__(host, model_name, task_name)
        self.decide_node_id = 0
        self.get_decide_node_id()

    def get_decide_node_id(self):
        """获取判定节点id"""
        url = self.host + "/api/v1/projects/" + str(self.project_id) + "/tasks/" + str(self.task_id) + "/task-config"
        res = self.session.request("get", url)
        self.decide_node_id = res['result']['decideNodeId']

    def start_execute(self, datasetId, datasetVersion, tags, gpuIndex = 0):
        """开始评估"""
        data = {
            "datasetId": datasetId,
            "datasetVersion": datasetVersion,
            "gpuIndex": gpuIndex,
            "tags": tags
        }
        url = self.host + f"/api/v1/projects/{str(self.project_id)}/tasks/{str(self.task_id)}/task-nodes/{self.decide_node_id}/start-execute"
        res = self.session.request("post", url, json=data)
        assert res["status"] == 0, f"评估失败，报错：{res["status"]}"

    def get_execute_result(self):
        """获取判定结果评估结果"""
        url = self.host + "/api/v1/projects/" + str(self.project_id) + "/tasks/" + str(self.task_id) + f"/task-nodes/{self.decide_node_id}/execute-result"
        res = self.session.request("get", url)
        return res['result']['list']

    def get_execute_result_image(self, imageKey):
        """获取判定结果评估结果图片详情"""
        url = self.host + "/api/v1/projects/" + str(self.project_id) + "/tasks/" + str(self.task_id) + f"/task-nodes/{self.decide_node_id}/execute-result/image"
        res = self.session.request("GET", url, params={"imageKey": imageKey})
        return res['result']['nodeList'][0]
