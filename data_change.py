

def str_to_dict(cookies):
    c_list_ = cookies.split(' ')
    c_list = [i.rstrip(';') for i in c_list_]
    cookies_dict = {i.split('=')[0]: i.split('=')[1] for i in c_list}
    return cookies_dict