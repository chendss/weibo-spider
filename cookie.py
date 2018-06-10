import CYDB
import weibo_api
import time


def cookie(user='15678594424', pwd='qianmeng520'):
    if 'self' in CYDB.all_table():
        data = CYDB.data('self', {'user': user})
        if str(data['cookie']) == '过期':
            update_cookie(user, pwd)
        else:
            pass
    else:
        cookie_ = weibo_api.login(user, pwd)
        CYDB.create_table('self', {
            'user': 'pk',
            'password': '',
            'cookie': '',
            'maxPage': '',
            'time': ''
        })
        CYDB.insert_data('self', {
            'time': 0,
            'user': user,
            'maxPage': '0',
            'password': pwd,
            'cookie': cookie_,
        })
    data = CYDB.data('self', {'user': user})
    cookie_ = data['cookie'].replace(' ', '')
    return cookie_


def update_cookie(user, pwd):
    cookie_ = weibo_api.login(user, pwd)
    CYDB.update_data('self', {
        'cookie': cookie_,
        'time': int(time.time() * 1000)
    }, {'user': user})
