import uuid

def generate_fe_uuid():
    # 生成标准的UUID4（随机UUID），转为字符串格式
    standard_uuid = str(uuid.uuid4())
    # 拼接FE-前缀，得到目标格式
    fe_uuid = f"FE-{standard_uuid}"
    return fe_uuid