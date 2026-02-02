from api.envCon import EnvCon

class TaskItem(EnvCon):

    def __init__(self, host, model_name, task_name):
        super().__init__(host)
        self.model_name = model_name
        self.task_name = task_name
        self.project_id = 0
        self.task_id = 0
        self.node_id = 0
        self.node_key = ""
        self.get_project_id()
        self.get_task_id()

    def get_project_id(self):
        """获取模型id"""
        url = self.host + "/api/v1/projects"
        res = self.session.request("get", url)
        project_list = res['result']['list']
        for item in project_list:
            if item['name'] == self.model_name:
                self.project_id = item['projectId']


    def get_task_id(self):
        """获取检测项id"""
        url = self.host + "/api/v1/projects/" + str(self.project_id) + "/tasks"
        res = self.session.request("get", url)
        task_list = res['result']['list']
        for item in task_list:
            if item['name']  == self.task_name:
                self.task_id = item['taskId']
                break

    def get_node_id(self, node_name="异常检测"):
        """获取节点版本配置"""
        url = self.host + "/api/v1/projects/" + str(self.project_id) + "/tasks/" + str(self.task_id) + "/pipeline"
        res = self.session.request("get", url)
        task_list = res['result']['nodes']
        for item in task_list:
            if item['name'] == node_name:
                self.node_key = item['key']
                self.node_id = item['id']
                return

    def get_ad_node_id(self, ad_node_name, version):
        """获取ad节点版本id"""
        self.get_node_id(ad_node_name)
        url = self.host + "/api/v1/projects/" + str(self.project_id) + "/tasks/" + str(
            self.task_id) + "/task-nodes/" + self.node_key + "/versions?pageSize=9999&pageNum=1&onlyVersion=true"
        res = self.session.request("get", url)
        version_list = res['result']['list']
        for item in version_list:
            if item['currentVersion'] == version:
                self.node_id = item['nodeId']
