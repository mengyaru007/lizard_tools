import os
from utils.log_util import logger

def get_image_file_obj(image_path):
    # 校验文件合法性
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片文件不存在：{image_path}")
    if not os.path.isfile(image_path):
        raise IsADirectoryError(f"路径不是文件：{image_path}")
    return open(image_path, 'rb')


def get_all_images_in_dir(dir_path: str, img_formats: tuple = None) -> list:
    """
    获取指定目录下所有图片的绝对路径（仅当前目录，不递归）
    :param dir_path: 目标目录路径（相对/绝对均可）
    :param img_formats: 要过滤的图片格式，默认支持jpg/jpeg/png/gif/bmp/webp
    :return: 图片绝对路径列表（如["D:/test/1.jpg", "D:/test/2.png"]）
    """
    # 默认支持的图片格式（小写，统一匹配）
    default_formats = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')
    img_formats = img_formats or default_formats

    # 初始化图片路径列表
    img_abs_paths = []

    # 校验目录是否存在
    if not os.path.isdir(dir_path):
        raise NotADirectoryError(f"指定路径不是目录：{dir_path}")

    # 遍历目录下所有文件
    for file_name in os.listdir(dir_path):
        # 拼接文件相对路径
        file_rel_path = os.path.join(dir_path, file_name)
        img_abs_paths.append(file_rel_path)

    return img_abs_paths


from itertools import islice


def split_list_by_chunk_iter(lst: list, chunk_size: int = 2000):
    """
    将列表按指定大小分块（迭代器版，内存友好）
    :param lst: 原始列表
    :param chunk_size: 每块大小
    :return: 迭代器，每次迭代返回一个分组列表
    """
    if not isinstance(lst, list):
        raise TypeError("输入必须是列表类型")
    if chunk_size <= 0:
        raise ValueError("分块大小必须大于0")

    # 将列表转为迭代器
    lst_iter = iter(lst)
    # 循环生成分组，直到迭代器为空
    while True:
        chunk = list(islice(lst_iter, chunk_size))
        if not chunk:
            break
        yield chunk