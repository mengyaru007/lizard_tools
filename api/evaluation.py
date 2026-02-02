from api.envCon import EnvCon

class Evaluation(EnvCon):

    def __init__(self, host):
        super().__init__(host)
        # 评估任务id
        self.evaluate_job_id = 0
        self.taskId = 0
        self.project_evaluation_job_id = 0
        self.get_evaluate_job_id()
        self.get_evaluate_job_info()

    def get_evaluate_job_id(self):
        """获取评估任务id"""
        url = self.host + "/api/v1/projects/evaluate-jobs"
        res = self.session.request("get", url)
        self.evaluate_job_id = res['result']['id']

    def get_evaluate_job_info(self):
        """获取评估任务相关信息"""
        url = self.host + f"/api/v1/project-evaluation/{self.evaluate_job_id}/inference-results"
        res = self.session.request("get", url)
        images_list = res['result']
        self.taskId = images_list[0]["taskId"]
        self.project_evaluation_job_id = images_list[0]["projectEvaluationJobId"]

    def get_normal_pictures(self):
        """获取ok图片列表{id:name}"""
        url = self.host + f"/api/v1/project-evaluation/{self.evaluate_job_id}/inference-results?type=normal"
        res = self.session.request("get", url)
        images_list= res['result']
        images_id_name = {}
        for imageInfo in images_list:
            images_id_name[imageInfo['id']] = imageInfo['name']
        return images_id_name

    def get_abnormal_pictures(self):
        """获取NG图片列表{id:name}"""
        url = self.host + f"/api/v1/project-evaluation/{self.evaluate_job_id}/inference-results?type=abnormal"
        res = self.session.request("get", url)
        images_list = res['result']
        images_id_name = {}
        for imageInfo in images_list:
            images_id_name[imageInfo['id']] = imageInfo['name']
        return images_id_name

