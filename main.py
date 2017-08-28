import api_weibo
import time
import json

def main():
    uid_dict = api_weibo.get_uid_list(1)[0]
    phots_url = api_weibo.get_photo_urls(uid_dict['uid'])[0]['urls']
    value = ( api_weibo.get_body(phots_url[0]) )
    print(value)


def get_all_album_dict():
    '''
    获得所有关注的人的专辑url
    '''
    uid_dict = api_weibo.get_uid_list(1)
    all_album_list = []
    for i in uid_dict:
        #time.sleep(2)
        photos = api_weibo.get_photo_urls( i['uid'] )
        print( i['name'] )
        all_album_list.append(photos)
    return all_album_list

main()