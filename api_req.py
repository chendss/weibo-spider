import CYDB
import time
import cookie
import requests
import data_change
import random
fuck_body=''

user = {
    'user': '15678594424',
    'pwd': 'qianmeng520'
}


def base_body(url, _cookie=None):
    """
    获得一个网页的返回值
    :param _cookie:
    :param url:空
    :return: body
    """
    _cookie = _cookie if _cookie is not None else cookie.cookie()
    cookies = data_change.str_to_dict(_cookie)

    s = requests.session()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/60.0.3112.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    r = s.get(url, cookies=cookies, headers=headers)
    text = r.text
    if text.count('微博-随时随地发现新鲜事') != 0:
        CYDB.update_data('self', {'cookie': '过期'}, {'user': user['user']})
        print('返回api的值是：',text)
        print('修改的cookie为：', CYDB.data('self', {'user': user['user']}))
        text = body(url)
    if text.count('用户不存在') !=0:
        print('这个请求怎么回事？',url)
        text=False
    elif text.count('try again')!=0:
        time.sleep(1)
        text = body(url)
    return text


def body(url, _cookie=None):
    try:
        self_body = base_body(url, _cookie)
        fuck_body = self_body
        return self_body
    except BaseException as error:
        print('api出现了一个异常啊？？：', error)
        time.sleep(random.randint(1,15))
        return None


def while_body(url, _cookie=None):
    """
    循环请求，直到返回正常值
    """
    while True:
        body_ = body(url,_cookie)
        if body_ is None:
            continue
        else:
            break
    return body_
