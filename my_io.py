import json

def write_uid(uid_name_dit):
    uid_json = json.dumps(uid_name_dit,ensure_ascii=False)
    with open('uid.txt', 'w') as f:
        f.write(uid_json)

def get_txt_dict(path):
    with open(f'{path}.txt') as f:
        text = json.loads(f.read())
    return text

def write_line_list(user_name,_list):
    print(_list)
    with open(f'user_dict\\{user_name}.txt','w') as f:
        for l in _list:
            f.write(l+'\n')
