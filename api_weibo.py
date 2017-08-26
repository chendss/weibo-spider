import data_change

def body(cookie,url):
    cookies_str = cookie
    cookies = str_to_dict(cookies_str)
    print('cookies:', cookies)

    s = requests.session()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    }

    r = s.get(url, cookies=cookies, headers=headers)
    print(r.status_code)
    # r.encoding='gbk'
    return  r.text

def get_userId(cookie,url):
    body = body(cookie,url)
    regx = regular_weibo.user()
    return_value = [a.split('\\"')[1] for a in regx.findall(body)]
    return return_value
