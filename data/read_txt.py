def read_txt(file_path):
    """
    读取txt文件内容，按行存储到列表中
    参数:file_path: txt文件的路径
    返回:包含文件各行内容的列表，如果发生错误则返回None
    """
    try:
        # 打开文件并按行读取
        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取所有行并去除每行末尾的换行符
            lines = [line.rstrip('\n') for line in file]
        return lines
    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 未找到")
    except Exception as e:
        print(f"读取文件时发生错误: {str(e)}")
    return None


if __name__ == "__main__":
    # 示例用法
    file_path = "add_train_images.txt"  # 替换为你的txt文件路径
    result = read_txt(file_path)

    if result is not None:
        print(f"成功读取文件，共 {len(result)} 行")
        print("文件内容列表:")
        print(result)
