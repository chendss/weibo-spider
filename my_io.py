import json

def write_uid(uid_name_dit):
    uid_json = json.dumps(uid_name_dit,ensure_ascii=False)
    with open('uid.txt', 'w') as f:
        f.write(uid_json)

def get_txt_dict(path):
    f = open(f'{path}.txt')
    text = json.loads(f.read())
    f.close()
    return text
