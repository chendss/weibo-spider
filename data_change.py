from time import time
import json

def str_to_dict(cookies):
    '''
    将cookie转换成dict
    cookie:从chrome复制下来的cookie
    '''
    c_list_ = cookies.split(' ')
    c_list = [i.rstrip(';') for i in c_list_]
    cookies_dict = {i.split('=')[0]: i.split('=')[1] for i in c_list}
    return cookies_dict

def get_rand():
    """
    返回一个特定的随机数
    经过测试，参数中的__rnd实际上是以毫秒为单位的时间戳
    """
    return int(round(time() * 1000))

def name_uid_dict(body,regx):
    '''
    将请求到的body转换成name和uid的字典
    regx:筛选的正则
    '''
    dict_1 = [a.split('\\"')[1] for a in regx.findall(body)]
    uid_name_dict = []
    for i in dict_1:
        uid = i.split('&')[0].split('=')[1]
        name = i.split('&')[1].split('=')[1]
        item = {
            'uid':uid,
            'name':name,
        }
        if item['name'] == '如落雨无声':
            continue
        uid_name_dict.append(item)
    return uid_name_dict

def photo_album_list(body,uid):
    '''
    将获得到的body转换成urls和page列表
    uid:当前微博的人的id
    '''
    album_list = json.loads(body)['data']['album_list']
    url_list = []
    for i in album_list:
        album_id = i['album_id']
        rand_time = get_rand()
        item = {
            'urls':[],
            'page':0,
        }
        item['page'] = int( i['count']['photos']/30 ) +1
        for i in range(1,item['page']+1):
            url = f'http://photo.weibo.com/photos/get_all?uid={uid}&album_id={album_id}&count=30&page={i}&type=18&__rnd={rand_time}'
            item['urls'].append(url)
        url_list.append(item)
    return url_list