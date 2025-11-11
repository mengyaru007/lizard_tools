"""截取图片名称中sn-部位-相机-时间"""

def extract_filename(filename):
    name_without_ext = filename.split('.')[0]
    # 按照双下划线分割
    parts = name_without_ext.split('__')
    # 取前四个部分并重新用双下划线连接
    if len(parts) >= 4:
        return '__'.join(parts[:4])
    else:
        return name_without_ext


if __name__ == "__main__":
    filename_test = "1816126197__sidewall3__camera8-light1-3__19751028183004490__NA_8_46.jpg"
    result = extract_filename(filename_test)
    print(f"原始文件名: {filename_test}")
    print(f"提取的部分: {result}")