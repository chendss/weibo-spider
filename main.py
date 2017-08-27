import api_weibo
import time
def main():
    uid_dict = api_weibo.get_uid_list()
    all_album_list = []
    for i in uid_dict:
        time.sleep(1)
        photos = api_weibo.get_photo_urls(i['uid'])
        all_album_list.append(photos)
    print(len(all_album_list))
main()