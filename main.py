import api_weibo

def main():
    uid_dict = api_weibo.get_uid_list()
    value = api_weibo.get_photo_url_by_uid(uid_dict[0]['uid'])
    print(value)
main()