import os
import shutil
folders = ["cavity-front", "cavity-side", "chafer1", "chafer2", "crown-groove1", "crown-groove2", "crown-groove3", "crown-groove4", "crown-surface", "sidewall1", "sidewall2", "sidewall3", "sidewall4"]

def copy_ng_image(parent_dir, output_dir):
    """
    copy导出的NG图片（image文件夹下的NG文件夹下）和NG信息图片（info-image文件夹下无NG文件夹）
    """
    for parent_folder in os.listdir(parent_dir):
        parent_path = os.path.join(parent_dir, parent_folder)
        for subfolder in os.listdir(parent_path):
            if "info" not in str(parent_folder):
                ng_image_folder = os.path.join(os.path.join(parent_path, subfolder), "NG")
                output_path = os.path.join(output_dir, "image")
            else:
                ng_image_folder = os.path.join(parent_path, subfolder)
                output_path = os.path.join(output_dir, "info_image")
            for ng_image_name in os.listdir(ng_image_folder):
                for folder_name in folders:
                    if folder_name in str(ng_image_name):
                        file_path = os.path.join(ng_image_folder, ng_image_name)
                        output_folder = os.path.join(output_path, folder_name)
                        os.makedirs(output_folder, exist_ok=True)
                        shutil.copy(file_path, output_folder)
                        print(f"  已复制: {file_path} -> {output_folder}")

# ============= 使用示例 =============
if __name__ == "__main__":
    parent_dir = "F:\\倍耐力轮胎\\1018-拍摄合集\\1018-OK中的NG导出-31PCS-part3"   # 修改为你的父文件夹路径
    output_dir = "F:\\倍耐力轮胎\\1018-拍摄合集\\1018-OK中的NG导出-ng-image"  # 输出文件夹路径
    copy_ng_image(parent_dir, output_dir)
