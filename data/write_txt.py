def write_txt(str_list, file_path):
    """
    将列表中的字符串按每行一个写入TXT文件
    str_list: 包含字符串的列表
    file_path: 要写入的文件路径
    """
    try:
        # 以写入模式打开文件，使用with语句自动处理文件关闭
        with open(file_path, 'w', encoding='utf-8') as file:
            # 遍历列表中的每个字符串
            for s in str_list:
                # 写入字符串并换行
                file.write(s + '\n')
        print(f"成功将 {len(str_list)} 个字符串写入文件: {file_path}")
    except Exception as e:
        print(f"写入文件时发生错误: {e}")


# 示例用法
if __name__ == "__main__":
    # 示例字符串列表
    example_list = [
        "第一行内容",
        "这是第二行",
        "Python编程",
        "将列表写入文件",
        "最后一行"
    ]
    # 调用函数将列表写入文件
    write_txt(example_list, "export_ng_images.txt")
