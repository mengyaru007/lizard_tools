import requests
class EnvCon:

    def __init__(self, host):
        self.host = host
        self.authorization = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.5YfhozPZ9Ca3sklCRoqm-yPeYkKdBB0katQdqngPORk"
        self.session = requests.Session()
        self.session.headers = {'Authorization': self.authorization}