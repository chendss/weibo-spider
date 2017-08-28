import requests
import json
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



def get_uid_list(page):
    ''' 
    获得当前页关注人列表
    返回一个带着name和uid的列表
    '''
    _url = f'http://weibo.com/p/1005052692248704/myfollow?t=1&cfs=&Pl_Official_RelationMyfollow__93_page={page}#Pl_Official_RelationMyfollow__93'
    body = get_body(_url)
    regx = regular_weibo.user()
    uid_name_dict = data_change.name_uid_dict(body,regx)
    return uid_name_dict


def get_photo_urls (uid):
    '''
    获得此用户图片专辑地址 
    uid:微博人id
    '''
    rand_time = data_change.get_rand()
    url = f'http://photo.weibo.com/albums/get_all?uid={uid}&page=1&count=20&__rnd={rand_time}'
    photo_dict = data_change.photo_album_list(get_body(url),uid)
    return photo_dict
