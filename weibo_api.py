import json
import CYDB
import time
import base64
import api_req
import CY_BjDB
import requests
import data_change


follow_url = 'https://m.weibo.cn/api/container/getSecond?containerid=1005052692248704_-_FOLLOWERS'


def login(username, password):
    """
    微博登陆函数
    :param username: 用户名
    :param password: 密码
    :return: 如果登陆成功返回cookies,失败返回None
    """
    username = base64.b64encode(username.encode('utf-8')).decode('utf-8')
    post_data = {
        'entry': 'sso',
        'gateway': '1',
        'from': 'null',
        'savestate': '30',
        'userticket': '0',
        'pagerefer': '',
        'vsnf': '1',
        'su': username,
        'service': 'sso',
        'sp': password,
        'sr': '1440*900',
        'encoding': 'UTF-8',
        'cdult': '3',
        'domain': 'sina.com.cn',
        'prelt': '0',
        'returntype': 'TEXT',
    }
    login_urL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    session = requests.Session()
    res = session.post(login_urL, data=post_data)
    json_str = res.content.decode('gbk')
    info = json.loads(json_str)
    if info["retcode"] == '0':
        # 把cookies添加到headers中，必须写这一步，否则后面调用API失败
        weibo_com_session = requests.Session()
        ret = weibo_com_session.get(info['crossDomainUrlList'][0])
        print(ret.content)
        cookies = ret.cookies.get_dict('.weibo.com', '/')
        cookies = [key + "=" + value for key, value in cookies.items()]
        cookies = "; ".join(cookies)
        print('登陆成功\n', cookies)
        return cookies
    else:
        print("登录失败，原因： %s" % info["reason"])
        return None


def follow(page=0):
    """
    获得关注的人的列表
    :param page: 当前页数
    :return: {uid,name}列表
    """
    print('开始获得关注人列表')
    uid_dict = []
    index_url = follow_url
    body = api_req.body(index_url)
    index_uid_dict = json.loads(body)
    # 设置请求的页数
    end_page = page if page != 0 else index_uid_dict['maxPage']  # 关注人最大页数
    url = 'https://m.weibo.cn/api/container/getSecond?containerid=1005052692248704_-_FOLLOWERS&page={}'
    for i in range(1, end_page + 1):
        print(f'获得关注人第{i}页开始')
        body = json.loads(api_req.body(url.format(i)))
        for b in body['cards']:
            item = {
                'uid': b['user']['id'],
                'name': b['user']['screen_name'],
            }
            uid_dict.append(item)
        print(f'获得关注人第{i}页结束')
    print('获得关注人列表结束')
    return uid_dict


def album(uid):
    """
    获得此用户图片专辑地址的列表
    :param uid: 此用户的id
    :return:{type,album_name,album_id,number,updateTime}的专辑列表
    """
    rand_time = data_change.get_rand()
    url = f'http://photo.weibo.com/albums/get_all?uid={uid}&page=1&count=20&__rnd={rand_time}'
    print(f'开始获得{uid}的专辑url', url)
    body = api_req.while_body(url)
    album_list_api = json.loads(body)['data']['album_list']
    if album_list_api is None or len(album_list_api) < 0:
        print(f'获得{uid}的专辑失败，将返回一个None', body, album_list_api)
        return None
    else:
        album_list = data_change.json_album(album_list_api)
        print(f'获得{uid}的专辑列表结束')
        print('\n')
        return album_list


def photos_by_album(album_dict, uid, page=0, cookie=None):
    """
    通过专辑信息获得第page页第图片列表
    :param album_dict:
    :param page:某一页
    :param uid:此人的id
    :return:包含此页数所有图片第url列表
    """
    rand_time = data_change.get_rand() + page
    base_page_url = 'http://photo.weibo.com/photos/get_all?uid={}&album_id={}&count=50&page={}&type={}&__rnd={}'
    page_url = base_page_url.format(
        uid, album_dict['album_id'], page, album_dict['type'], rand_time)
    page_json = api_req.while_body(page_url, cookie)
    if page_json is None or page_json == False:
        return []
    return_value = []
    try:
        return_value = data_change.page_json_to_photos(page_json)
    except BaseException as error:
        print('data_change.page_json_to_photos(page_json)发生了一个异常，异常信息是：\n', error)
        for i in range(0, 1500):
            print('api返回的值是：', page_json)
            time.sleep(5)
        raise BaseException('抛出一个异常')
    return return_value


def update_follow(page=6):
    """
    更新关注
    :return:
    """
    return follow(page)


def update_album(uid):
    """
    更新专辑列表
    :param uid:
    :return:
    """
    pass


def max_page():
    """
    获得最大页数
    :return:
    """
    index_url = follow_url
    body = api_req.body(index_url)
    index_uid_dict = json.loads(body)
    # 设置请求的页数
    return index_uid_dict['maxPage']  # 关注人最大页数
