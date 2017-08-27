import data_change
import regular_weibo
import requests
import regular_weibo
from cookie import get_cookie

_cookie = get_cookie()

def get_body(url):
    cookies = data_change.str_to_dict(_cookie)
    print('cookies:', cookies)

    s = requests.session()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    }

    r = s.get(url, cookies=cookies, headers=headers)
    print(r.status_code)
    # r.encoding='gbk'
    return  r.text



def get_uid_list(url='http://weibo.com/p/1005052692248704/myfollow?t=1&cfs=&Pl_Official_RelationMyfollow__111_page=10'):
    '''获得当前页关注人列表'''
    body = get_body(url)
    regx = regular_weibo.user()
    list_1 = [a.split('\\"')[1].rstrip('&') for a in regx.findall(body)]
    return_value = []
    for i in list_1:
        uid = i.split('&')[0].split('=')[1]
        name = i.split('&')[1].split('=')[1]
        item = {
            'uid':uid,
            'name':name,
        }
        return_value.append(item)
    return return_value


def get_photo_url_by_uid (uid):
    '''获得此用户图片地址'''
    # url = f'http://photo.weibo.com/{uid}/albums'
    url = 'http://photo.weibo.com/albums/get_all?uid=3305836581&page=1&count=20&__rnd=1503827709022'
    body = get_body(url)
    
    return body
