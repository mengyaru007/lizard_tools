import cv2
from PIL import Image

def save_chinese_path(save_path, img):
        cropped_image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
                pil_img = Image.fromarray(cropped_image_rgb)
                pil_img.save(save_path)
                print(f"保存成功：{save_path}")
        except Exception as e:
                print(f"保存失败：{e}，路径：{save_path}")