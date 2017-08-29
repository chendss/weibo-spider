import requests
import json
import time
import data_change
import regular_weibo
import regular_weibo
from cookie import get_cookie


_cookie = get_cookie()

def get_body(url):
    cookies = data_change.str_to_dict(_cookie)
    # print('cookies:', cookies)

    s = requests.session()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest',
    }

    r = s.get(url, cookies=cookies, headers=headers)
    print(r.status_code)
    # r.encoding='gbk'
    return  r.text

def create_uid_name_dict (page=0) :
    uid_dict = [] 
    index_url = f'https://m.weibo.cn/api/container/getSecond?containerid=1005052692248704_-_FOLLOWERS'
    index_uid_dict = json.loads (get_body(index_url) )
    # 设置请求的页数
    if page != 0 :
        max_page = page
    else :
        max_page = index_uid_dict['maxPage'] #关注人最大页数
    #
    for i in range(max_page+1):
        url = f'https://m.weibo.cn/api/container/getSecond?containerid=1005052692248704_-_FOLLOWERS&page={i}'
        body = json.loads( get_body(url) )
        for b in body['cards']:
            item = {
                'uid' : b['user']['id'],
                'name' : b['user']['screen_name'],
            }
            uid_dict.append(item)
    return uid_dict



def get_photo_urls (uid):
    '''
    获得此用户图片专辑地址 
    uid:微博人id
    '''
    rand_time = data_change.get_rand()
    url = f'http://photo.weibo.com/albums/get_all?uid={uid}&page=1&count=20&__rnd={rand_time}'
    photo_dict = data_change.photo_album_list(get_body(url),uid)
    return photo_dict

def get_album_photo_list(album_url):
    print(album_url)
    while True:
        try:
            body = get_body(album_url)
            break
        except:
            time.sleep(2)
            continue
    if body == None:
        return None
    photo_list = json.loads(body)['data']['photo_list']
    photo_s = [potot_url['pic_name'] for potot_url in photo_list]
    return_value = data_change.p_ids_to_purl_list(photo_s)
    return return_value