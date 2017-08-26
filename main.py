import requests
import regular_weibo
import api_weibo

def get_userId(cookie):
    body = api_weibo.body(cookie,'url')
    regx = regular_weibo.user()
    return_value = [a.split('\\"')[1] for a in regx.findall(body)]
    return return_value

def main():
    cookie = 'your cookie'
    items = get_userId(cookie)
    print(items)

main()