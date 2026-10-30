"""方向，角色面对的哪个方向"""

face = "left"  # 朝向
LEFT = "left"
RIGHT = "right"


def set_face_left():
    """设置朝向左"""
    global face
    face = LEFT


def set_face_right():
    """设置朝向左"""
    global face
    face = RIGHT


def is_left():
    return face == LEFT


def is_right():
    return face == RIGHT
