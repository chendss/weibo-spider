import api_weibo
from cookie import cookie

def main():
    items = api_weibo.get_uid_list(cookie)
    print(items)

main()