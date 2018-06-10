import CYDB
import time
import queue
import cookie
import CY_BjDB
import weibo_api
import threading
import data_change


user = {
    'user': '15678594424',
    'pwd': 'qianmeng520'
}


def init(user, pwd):
    if 'self' not in CYDB.all_table() or str(CYDB.data('self', {'user': user})['time']) != '0':
        pass
    else:
        cookie_ = cookie.cookie(user, pwd)
        max_page = weibo_api.max_page()
        print('关注人最大页数是：', max_page)
        CYDB.update_data('self', {
            'time': int(time.time() * 1000),
            'cookie': cookie_,
            'maxPage': 0
        }, {'user': str(user)})


# 关注人


def update_follow(user):
    """
    写关注人到sqlite数据库
    :param user:
    :return:
    """
    print('开始写关注人')
    if 'user' in CYDB.all_table():
        pass
    else:
        CYDB.create_table('user', {
            'uid': 'pk',
            'name': '',
            'album': ''
        })
    get_page = follow_page(user)
    print('需要获取的页数是：', get_page)
    follow_insert_db(get_page)
    print('更新关注人结束')


def follow_page(user):
    """
    返回需要获取关注人的页数
    :param user:
    :return:
    """
    max_page = int(weibo_api.max_page())
    db_page = int(CYDB.data('self', {'user': user})['maxPage'])
    page_ = max_page - db_page
    if page_ > 0:
        CYDB.update_data('self', {
            'maxPage': max_page,
            'time': int(time.time() * 1000)
        }, {'user': str(user)})
        if page_ == max_page:
            page_ = max_page
        else:
            page_ = page_ + 2
    else:
        page_ = 3
    return page_


def follow_insert_db(page_):
    """
    增量插入数据库
    :param page_:
    :return:
    """
    follow_list = weibo_api.follow(page_)
    for p in follow_list:
        CYDB.insert_data('user', {
            'uid': str(p['uid']),
            'name': p['name']
        })


# 专辑

def update_album(uid, _table_list=None):
    """
    将专辑信息写入数据库
    :param uid:
    :return:
    """
    table_list = set(CYDB.all_table()) if _table_list is None else _table_list
    table_name = f'A{uid}'
    if table_name in table_list:
        pass
    else:
        CYDB.create_table(table_name, {
            'type': '',
            'number': '',
            'album_id': 'pk',
            'album_name': '',
            'updateTime': '',
        })
        CYDB.update_data('user', {'album': table_name}, {'uid': uid})
        album_list = weibo_api.album(uid)
        for album in album_list:
            album['album_name'] = data_change.str_del(album['album_name'])
            album_id = str(album['album_id'])
            has_album_id = False if CYDB.data(
                table_name, {'album_id': album_id}) is None else True
            if has_album_id:
                CYDB.update_data(f'A{uid}', album, {'album_id': album_id})
            else:
                CYDB.insert_data(f'A{uid}', album)


# 图片url

def update_photo(uid_list, cookie, table_list):
    """
    获得多个专辑的图片的url
    """
    thread_setting_dict = thread_list_start(uid_list, cookie, table_list)
    count = 0
    for uid in uid_list:
        if f'P{uid}' in table_list:
            continue
        photos = []
        table_name = f'P{uid}'
        for q in thread_setting_dict[table_name]:
            photos.extend(q.get())
        photos = list(set(photos))
        count = count + len(photos)
        CYDB.create_table(table_name, {'url': 'pk'})
        CYDB.insert_batch(table_name, 'url', [(photo,) for photo in photos])
    print('本次写入图片数量是：', count)
    if count == 0:
        return False
    else:
        return True


def thread_list_start(uid_list, cookie, table_list):
    """
    启动线程
    """
    thread_setting_dict = thread_setting(uid_list, cookie, table_list)
    thread_list = thread_setting_dict['thread_list']
    thread_list_list = [thread_list[i:i + 64]
                        for i in range(0, len(thread_list), 64)]
    i = 0
    for t_l in thread_list_list:
        i = i + 1
        for t in t_l:
            t.start()
        for t in t_l:
            t.join()
        print(f'{i}次请求已完成', len(thread_list_list))
    return thread_setting_dict


def thread_setting(uid_list, cookie, table_list):
    """
    获得多线程配置
    """
    thread_dict = {
        'thread_list': []
    }
    for uid in uid_list:
        if f'P{uid}' in table_list:
            continue
        album_list = CYDB.table(f'A{uid}')
        thread_dict[f'P{uid}'] = []
        for album in album_list:
            max_page = int(int(album['number']) / 50) + 1
            for i in range(0, max_page):
                q = queue.Queue()
                t = threading.Thread(target=page_photos,
                                     args=(album, uid, i, q, cookie,))
                thread_dict[f'P{uid}'].append(q)
                thread_dict['thread_list'].append(t)
    return thread_dict


def page_photos(album, uid, page, q, cookie):
    """
    请求专辑某一页
    """
    page_photos = weibo_api.photos_by_album(album, uid, page, cookie)
    q.put(list(set(page_photos)))


# 图片更新
