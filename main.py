import api_weibo
import json
import my_io
import data_judge

def main():
    uid_name_dit = my_io.get_uid_name_dict('uid')
    print(data_judge.is_has_dict('5651275769',uid_name_dit))
main()