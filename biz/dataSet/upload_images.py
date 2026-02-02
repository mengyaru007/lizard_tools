"""数据集上传图片"""
from api.dataSet import DataSet
from utils.file_obj import get_all_images_in_dir, split_list_by_chunk_iter
from utils.log_util import logger
import time

def upload(dataset, image_path, random_num):
    """上传图片"""
    try:
        files = dataset.upload_image(image_path, random_num)
        return files
    except Exception as e:
        logger.warning(f"{image_path}图片上传失败！报错原因={e}")

def import_images(dataset, images_path, tags=None):
    """导入已上传的图片"""
    random_num = int(time.time() * 1000)
    files = []
    total_img = len(images_path)
    uploaded_img = 0
    logger.info(f"【图片导入-开始】 本组待导入图片数：{total_img} | 标签：{tags}")
    for image in images_path:
        files.extend(upload(dataset, image, random_num))
        uploaded_img += 1
        progress_percent = (uploaded_img / total_img) * 100
        # 打印逐张上传进度日志
        logger.info(
            f"【图片上传-进度】[{uploaded_img}/{total_img}] "
            f"({progress_percent:.2f}%) | 成功上传：{image}"
        )
    dataset.import_tasks(files, random_num, tags)

def upload_images(host, dataset_name, version, tag, file_path):
    images_path = get_all_images_in_dir(file_path)
    # 迭代器分组（不会一次性生成所有组，内存占用低）
    image_chunk_iter = split_list_by_chunk_iter(images_path, chunk_size=2000)
    dataset = DataSet(host, dataset_name, version)
    for idx, chunk in enumerate(image_chunk_iter, 1):
        tags = [f"{tag}-{idx}"]
        logger.info(f"开始导入第{idx}组图片：{len(chunk)}")
        import_images(dataset, chunk, tags)


if __name__ == "__main__":
    upload_images("http://10.110.156.90:9012/", "myr-test", "1", "0112", "C:\\Users\mengyr1\Desktop\\test")