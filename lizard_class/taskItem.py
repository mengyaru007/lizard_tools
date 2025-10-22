from lizard_class.envCon import EnvCon

class TaskItem(EnvCon):

    def __init__(self, host, model_name, task_name):
        super().__init__(host)
        self.model_name = model_name
        self.task_name = task_name
        self.project_id = 0
        self.task_id = 0
        self.node_id = 0
        self.get_project_id()
        self.get_task_id()

    def get_project_id(self):
        """获取模型id"""
        url = self.host + "/api/v1/projects"
        print(f"请求接口{url}")
        res = self.session.request("get", url).json()
        print(f"{url}的响应数据：{res}")
        project_list = res['result']['list']
        for item in project_list:
            if item['name'] == self.model_name:
                self.project_id = item['projectId']


    def get_task_id(self):
        """获取检测项id"""
        url = self.host + "/api/v1/projects/" + str(self.project_id) + "/tasks"
        print(f"请求接口{url}")
        res = self.session.request("get", url).json()
        print(f"{url}的响应数据：{res}")
        task_list = res['result']['list']
        for item in task_list:
            if item['name']  == self.task_name:
                self.task_id = item['taskId']
                break

    def get_node_id(self, version=0, node_name="异常检测"):
        """获取节点版本id"""
        url = self.host + "/api/v1/projects/" + str(self.project_id) + "/tasks/" + str(self.task_id) + "/pipeline"
        print(f"请求接口{url}")
        res = self.session.request("get", url).json()
        print(f"{url}的响应数据：{res}")
        task_list = res['result']['nodes']
        node_key = ""
        for item in task_list:
            if item['name'] == node_name:
                node_key = item['key']
                if node_name == "分类":
                    self.node_id = item['id']
                break
        if node_name == "异常检测":
            url = self.host + "/api/v1/projects/" + str(self.project_id) + "/tasks/" + str(self.task_id) + "/task-nodes/" + node_key + "/versions?pageSize=9999&pageNum=1&onlyVersion=true"
            print(f"请求接口{url}")
            res = self.session.request("get", url).json()
            print(f"{url}的响应数据：{res}")
            version_list = res['result']['list']
            for item in version_list:
                if item['currentVersion'] == version:
                    self.node_id = item['nodeId']
