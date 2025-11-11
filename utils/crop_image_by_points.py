"""
根据标注裁剪图片
"""
import cv2
import numpy as np

def crop_image_by_points(image_path, points):
    # 读取图片
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"无法读取图片: {image_path}")
    # 创建掩码
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    points = np.array([points], dtype=np.int32)
    # 填充多边形区域
    cv2.fillPoly(mask, points, 255)
    # 应用掩码
    masked_image = cv2.bitwise_and(image, image, mask=mask)
    # 计算边界矩形并裁剪
    x, y, w, h = cv2.boundingRect(points)
    cropped_image = masked_image[y:y + h, x:x + w]
    return cropped_image