import logging
import os
from logging.handlers import TimedRotatingFileHandler
from colorlog import ColoredFormatter

# 项目根目录（适配分层结构，和conf/config.py的BASE_DIR一致）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 日志文件存储目录
LOG_DIR = os.path.join(BASE_DIR, "logs")
# 若日志目录不存在则创建
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def init_log(level: str = "INFO") -> logging.Logger:
    """
    初始化日志配置：控制台彩色输出 + 本地文件按天分割保存
    :param level: 日志级别，默认INFO（可选：DEBUG/INFO/WARNING/ERROR/CRITICAL）
    :return: 全局日志对象
    """
    # 定义日志级别映射
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    log_level = level_map.get(level.upper(), logging.INFO)

    # 1. 创建全局日志对象，设置根级别
    logger = logging.getLogger("lizard_tools")  # 项目名作为日志器名称，避免和其他日志冲突
    logger.setLevel(log_level)
    # 避免重复添加处理器（多次调用init_log时）
    if logger.handlers:
        logger.handlers.clear()

    # 2. 定义日志格式
    # 文件日志格式：[时间] [级别] [模块:行号] 内容
    file_formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    # 控制台彩色日志格式：[时间] [彩色级别] [模块:行号] 彩色内容
    color_formatter = ColoredFormatter(
        fmt="%(log_color)s%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s%(reset)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",  # info级日志标为绿色，重点突出
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red"
        }
    )

    # 3. 创建文件处理器：按天分割日志，保留7天，编码utf-8（避免中文乱码）
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(LOG_DIR, "interface_auto.log"),  # 日志文件名
        when="D",  # 按天分割（可选：S/秒 M/分 H/时 D/天 W/周）
        interval=1,  # 每1个单位分割一次
        backupCount=7,  # 保留7天的日志文件
        encoding="utf-8"
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(file_formatter)

    # 4. 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(color_formatter)

    # 5. 将处理器添加到日志对象
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# 全局初始化日志对象（默认INFO级别，项目中所有模块直接导入该对象即可）
logger = init_log(level="DEBUG")

# ------------------- 接口自动化专用：便捷打印请求/响应的info日志 -------------------
def log_request_info(url: str, method: str, params: dict = None, data: dict = None, files: dict = None):
    """
    打印接口请求的info级日志（适配GET/POST，含参数/文件）
    :param url: 请求URL
    :param method: 请求方法（GET/POST/PUT/DELETE）
    :param params: URL参数（GET请求）
    :param data: 表单/JSON参数（POST请求）
    :param files: 文件参数（上传接口）
    """
    logger.info(f"【接口请求】方法：{method.upper()}，URL：{url}")
    if params:
        logger.info(f"【请求参数】URL参数：{params}")
    if data:
        logger.info(f"【请求参数】表单/JSON参数：{data}")
    if files:
        # 打印文件参数时只显示文件名，避免打印二进制内容
        file_info = {k: v[0] for k, v in files.items()} if files else None
        logger.info(f"【请求参数】文件参数：{file_info}")

def log_response_info(status_code: int, response: dict, elapsed: float = None):
    """
    打印接口响应的info级日志
    :param status_code: HTTP状态码
    :param response: 响应JSON数据
    :param elapsed: 请求耗时（秒，可选）
    """
    logger.info(f"【接口响应】状态码：{status_code}")
    if elapsed:
        logger.info(f"【请求耗时】{elapsed:.3f} 秒")
    logger.info(f"【响应数据】{response}")