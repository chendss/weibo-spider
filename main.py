import api_weibo
import json
import my_io
import data_judge
import data_change

def get_uid_photo(uid):
    _p_url_list = []
    photos = api_weibo.get_photo_urls(uid)
    for urls_item_list in photos:
        for a_url in urls_item_list['urls']:
            p_url_list = api_weibo.get_album_photo_list(a_url)
            print(p_url_list)
    return _p_url_list

def main():
    uid = my_io.get_txt_dict('uid')[0]['uid']
    p = api_weibo.get_photo_urls(uid)[2]['urls'][0]
    value = api_weibo.get_album_photo_list(p)
    print(value)
main()