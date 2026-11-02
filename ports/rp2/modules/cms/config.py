mode = 3
"""
mode: 1   固件程序控制
mode: 2   树莓派 uart 通讯控制
mode: 3   固件程序 + 树莓派 uart 通讯

"""

comfig_map = {
    "face": "right",
}


def setMode(_mode):
    global mode
    mode = _mode


def getMode():
    return comfig_map.get("mode", 1)


def setKeyValue(key, value):
    return comfig_map.update(key, value)
