import re

def user():
    reg_1 = 'action-data=\\\\"'
    reg_2 = 'uid=\d+&fnick=' # 匹配用户ID
    reg_3 = '[\u4e00-\u9fa5_a-zA-Z0-9]+&' #匹配用户名-中英文
    regx = re.compile(reg_1+reg_2+reg_3)
    return regx