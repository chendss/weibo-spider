import api_weibo

def main():
    uid_dict = api_weibo.get_uid_list()
    value = api_weibo.get_photo_urls(uid_dict[2]['uid'])
    print(uid_dict[2]['name'],uid_dict[2]['uid'])
    print(value)
main()