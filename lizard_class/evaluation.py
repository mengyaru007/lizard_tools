from lizard_class.envCon import EnvCon

class Evaluation(EnvCon):

    def __init__(self, host):
        super().__init__(host)
        # 评估任务id
        self.evaluate_job_id = 0
        self.task = 0
        self.project_evaluation_job_id = 0
        self.get_evaluate_job_id()
        self.get_evaluate_job_info()

    def get_evaluate_job_id(self):
        """获取评估任务id"""
        url = self.host + "/api/v1/projects/evaluate-jobs"
        print(f"请求接口{url}")
        res = self.session.request("get", url).json()
        print(f"{url}的响应数据：{res}")
        self.evaluate_job_id = res['result']['id']

    def get_evaluate_job_info(self):
        """获取评估任务相关信息"""
        images = self.get_normal_pictures()
        images.update(self.get_abnormal_pictures())
        images_list = list(images.values())
        self.task = images_list[0]["taskId"]
        self.project_evaluation_job_id = images_list[0]["projectEvaluationJobId"]

    def get_normal_pictures(self):
        """获取ok图片列表{id:name}"""
        url = self.host + f"/api/v1/project-evaluation/{self.evaluate_job_id}/inference-results?type=normal"
        print(f"请求接口{url}")
        res = self.session.request("get", url).json()
        print(f"{url}的响应数据：{res}")
        image_list= res['result']['list']
        images_id_name = {}
        for imageInfo in image_list:
            images_id_name[imageInfo['id']] = imageInfo['name']
        print(f"OK图片总共{len(images_id_name)}个图片！")
        return images_id_name

    def get_abnormal_pictures(self):
        """获取NG图片列表{id:name}"""
        url = self.host + f"/api/v1/project-evaluation/{self.evaluate_job_id}/inference-results?type=abnormal"
        print(f"请求接口{url}")
        res = self.session.request("get", url).json()
        print(f"{url}的响应数据：{res}")
        image_list = res['result']['list']
        images_id_name = {}
        for imageInfo in image_list:
            images_id_name[imageInfo['id']] = imageInfo['name']
        print(f"NG图片总共{len(images_id_name)}个图片！")
        return images_id_name

