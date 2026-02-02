from utils.request_utils import req

authorization = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.5YfhozPZ9Ca3sklCRoqm-yPeYkKdBB0katQdqngPORk"
req.headers = {'Authorization': authorization}

class EnvCon:

    def __init__(self, host):
        self.host = host
        self.session = req

    def get_host_info(self):
        """获取环境GPU配置"""
        url = self.host + "/api/v1/info/host"
        res = self.session.request("get", url)
        return res["gpuList"]