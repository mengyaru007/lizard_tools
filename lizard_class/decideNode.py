from lizard_class.taskItem import TaskItem

class DecideNode(TaskItem):

    def __init__(self, host, model_name, task_name):
        super().__init__(host, model_name, task_name)
        self.decide_node_id = 0
        self.get_decide_node_id()

    def get_decide_node_id(self):
        """获取判定节点id"""
        url = self.host + "/api/v1/projects/" + str(self.project_id) + "/tasks/" + str(self.task_id) + "/task-config"
        print(f"请求接口{url}")
        res = self.session.request("get", url).json()
        print(f"{url}的响应数据：{res}")
        self.decide_node_id = res['result']['decideNodeId']

    def get_execute_result(self):
        """获取判定结果评估结果"""
        url = self.host + "/api/v1/projects/" + str(self.project_id) + "/tasks/" + str(self.task_id) + f"/task-nodes/{self.decide_node_id}/execute-result"
        print(f"请求接口{url}")
        res = self.session.request("get", url).json()
        print(f"{url}的响应数据：{res}")
        return res['result']['list']

    def get_execute_result_image(self, imageKey):
        """获取判定结果评估结果图片详情"""
        url = self.host + "/api/v1/projects/" + str(self.project_id) + "/tasks/" + str(self.task_id) + f"/task-nodes/{self.decide_node_id}/execute-result/image"
        print(f"请求接口{url},imageKey={imageKey}")
        res = self.session.request("GET", url, params={"imageKey": imageKey}).json()
        print(f"{url}的响应数据：{res}")
        return res['result']['nodeList'][0]
