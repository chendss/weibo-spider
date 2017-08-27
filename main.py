import api_weibo
from cookie import get_cookie

def main():
    items = api_weibo.get_uid_list(get_cookie())
    print(items)

main()