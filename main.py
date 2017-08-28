import api_weibo
import json
import time

def main():
    index_url = f'https://m.weibo.cn/api/container/getSecond?containerid=1005052692248704_-_FOLLOWERS'
    index_uid_dict = json.loads (api_weibo.get_body(index_url) )
    max_page = index_uid_dict['maxPage']
    uid_dict = []
    z = 0
    for i in range(1):
        url = f'https://m.weibo.cn/api/container/getSecond?containerid=1005052692248704_-_FOLLOWERS&page={i}'
        t1 = time.time()
        body = json.loads( api_weibo.get_body(url) )
        print('请求时间：',time.time()-t1)
        t1 = time.time()
        for b in body['cards']:
            item = {
                'uid' : b['user']['id'],
                'name' : b['user']['screen_name'],
            }
            uid_dict.append(item)
    print(uid_dict)
    uid_json = json.dumps(uid_dict)
    with open('uid.txt', 'w') as f:
        f.write(uid_json)
main()