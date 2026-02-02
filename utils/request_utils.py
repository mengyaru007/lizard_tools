import requests
from typing import Optional, Dict, Any
from requests import RequestException, Response
from utils.log_util import logger  # 导入之前封装的全局日志对象

# 定义通用参数类型，简化注解
Headers = Optional[Dict[str, str]]
Params = Optional[Dict[str, Any]]
Data = Optional[Dict[str, Any]]
Files = Optional[Dict[str, Any]]
Json = Optional[Dict[str, Any]]


class RequestUtil:
    """
    Requests极简封装：单入口request方法 + Debug日志 + 异常处理 + 自动JSON解析
    直接使用self.session.request(method, url)原生形式，适配所有请求类型
    """
    def __init__(self, timeout: int = 30):
        # 初始化Session，复用连接、自动处理Cookies
        self.session = requests.Session()
        # 全局超时时间，所有请求默认生效，可单独覆盖
        self.timeout = timeout
        self.session.headers = {}

    def _print_debug_log(self, method: str, url: str, **kwargs) -> None:
        """私有方法：打印请求Debug日志（日志级别为DEBUG时生效）"""
        if logger.level > 10:  # 日志级别>DEBUG(10)时，不打印Debug日志
            return
        # 拼接请求Debug日志，分行打印更清晰
        debug_log = f"\n【DEBUG-请求信息】"
        debug_log += f"\n├─ 请求方法：{method.upper()}"
        debug_log += f"\n├─ 请求URL：{url}"
        params = kwargs.get("params")
        if params:
            debug_log += f"\n├─ URL参数：{params}"
        json= kwargs.get("json")
        if json:
            debug_log += f"\n├─ JSON参数：{json}"
        data = kwargs.get("data")
        if data:
            debug_log += f"\n├─ Form参数：{data}"
        files = kwargs.get("files")
        if files:
            # 文件参数仅打印文件名，避免二进制流污染日志
            file_info = {k: v[0] if isinstance(v, tuple) else v for k, v in files.items()}
            debug_log += f"\n├─ 文件参数：{file_info}"
        logger.debug(debug_log)

    def _print_response_log(self, response: Response) -> None:
        """私有方法：打印响应Debug日志（日志级别为DEBUG时生效）"""
        if logger.level > 10:
            return
        # 拼接响应Debug日志
        res_log = f"\n【DEBUG-响应信息】"
        res_log += f"\n├─ 状态码：{response.status_code}"
        res_log += f"\n├─ 响应头：{dict(response.headers)}"
        res_log += f"\n├─ 请求耗时：{response.elapsed.total_seconds():.3f} 秒"
        res_log += f"\n├─ 实际请求URL：{response.url}"
        try:
            # 尝试解析JSON，格式化打印
            res_json = response.json()
            res_log += f"\n└─ 响应体(JSON)：{res_json}"
        except Exception:
            # 非JSON响应打印原始文本（截断过长内容，避免日志过大）
            res_text = response.text[:500] + "..." if len(response.text) > 500 else response.text
            res_log += f"\n└─ 响应体(原始)：{res_text}"
        logger.debug(res_log)

    def request(self, method: str, url: str,
                params: Params = None,
                data: Data = None,
                json: Json = None,
                files: Files = None,
                headers: Headers = None,
                timeout: Optional[int] = None,
                **kwargs) -> Dict[str, Any]:
        """
        通用请求方法：核心封装，直接调用session.request，适配所有请求类型
        :param method: 请求方法，如get/post/put/delete（大小写均可）
        :param url: 请求URL
        :param params: URL拼接参数，如?page=1&size=10
        :param data: Form表单参数（form-data/x-www-form-urlencoded）
        :param json: JSON请求体，自动设置Content-Type: application/json
        :param files: 文件上传参数，格式{"file": (文件名, 二进制流, MIME类型)}
        :param headers: 请求头，如{"Authorization": "Bearer token"}
        :param timeout: 单个请求超时时间，覆盖全局timeout
        :param kwargs: 其他requests原生参数，如allow_redirects/proxies等
        :return: 接口响应JSON字典（自动化主流场景）
        :raise: RequestException 所有请求异常统一抛出
        """
        # 初始化请求参数，过滤空值（避免传递空字典给requests）
        req_kwargs = {
            "params": params or {},
            "data": data or {},
            "json": json or {},
            "files": files or {},
            "headers": headers or {},
            "timeout": timeout or self.timeout,
            **kwargs  # 接收其他原生参数，保持灵活性
        }
        # 过滤值为{}或None的参数，减少冗余请求
        req_kwargs = {k: v for k, v in req_kwargs.items() if v not in [{}, None]}

        try:
            # 1. 打印请求Debug日志
            self._print_debug_log(method, url, **req_kwargs)
            # 2. 核心：调用session.request原生方法，传入method和url
            response: Response = self.session.request(
                method=method.lower(),  # 统一转小写，避免方法名大小写问题
                url=url,
                **req_kwargs
            )
            # 3. 打印响应Debug日志
            self._print_response_log(response)
            # 4. 校验HTTP状态码，4xx/5xx直接抛出HTTPError
            response.raise_for_status()
            # 5. 自动解析JSON响应（接口自动化主流场景）
            return response.json()

        except RequestException as e:
            # 捕获所有requests异常：连接/超时/HTTP错误/JSON解析错误等
            error_msg = f"[{method.upper()}] {url} 请求失败：{str(e)}"
            # 记录错误日志，打印异常堆栈（便于定位问题）
            logger.error(error_msg, exc_info=True)
            # 统一抛出异常，让上层（api/biz/用例层）处理
            raise RequestException(error_msg) from e

    def close(self) -> None:
        """关闭Session，释放网络连接资源"""
        self.session.close()
        logger.debug("Requests Session已关闭，释放连接资源")


# 实例化全局请求对象，项目所有模块直接导入该对象使用，无需重复实例化
req = RequestUtil()