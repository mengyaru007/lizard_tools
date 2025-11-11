"""
计算多边形的外接矩形
points: 多边形顶点列表，格式为 [(x1,y1), (x2,y2), ..., (xn,yn)]
"""

def get_bounding_rect(points):
    if not points:  # 避免空列表报错
        return None

    # 提取所有x和y坐标
    x_coord = [p[0] for p in points]
    y_coord = [p[1] for p in points]

    # 计算外接矩形的边界（最小/最大坐标）
    x_min = min(x_coord)  # 左上角x
    y_min = min(y_coord)  # 左上角y
    x_max = max(x_coord)  # 右下角x
    y_max = max(y_coord)  # 右下角y

    # 返回外接矩形的参数（左上角坐标 + 宽高）
    return {
        "x": x_min,
        "y": y_min,
        "width": x_max - x_min,  # 宽 = 最大x - 最小x
        "height": y_max - y_min  # 高 = 最大y - 最小y
    }