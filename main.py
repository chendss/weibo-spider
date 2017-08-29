import api_weibo
import json
import my_io
import data_judge
import data_change

def get_uid_photo(uid):
    p_url_list_big = []
    photos = api_weibo.get_photo_urls(uid)
    for urls_item_list in photos:
        for a_url in urls_item_list['urls']:
            url_list = api_weibo.get_album_photo_list(a_url)
            p_url_list = url_list if url_list else []
            p_url_list_big.extend(p_url_list)
    return p_url_list_big

def get_all_user_urls():
    dict_ = my_io.get_txt_dict('uid')
    for d in dict_:
        uid = d['uid']
        name = d['name']
        test = get_uid_photo(uid)
        my_io.write_line_list(name,test)

def main():
    get_all_user_urls()
    
main()