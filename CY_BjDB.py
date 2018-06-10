from bjdb import BJDB, Query

db = BJDB('weibo_bj.db', ['uid', 'name'])
query = Query()


def all_table():
    """
    返回所有表名
    :return:
    """
    return db.tables()


def i_data(data_dict, table_name=''):
    """
    插入一条数据
    :param data_dict: 键：值
    :param table_name: 
    :return: 
    """
    if table_name == '':
        db.insert(data_dict)
    else:
        db.insert(data_dict, table=table_name)


def i_batch_data(data_dict_list, table_name=''):
    """
    对一张表批量插入数据
    :param data_dict_list:[{键:值},{键:值},……,{键:值}]
    :param table_name:
    :return:
    """
    for data_dict in data_dict_list:
        i_data(data_dict, table_name)


def data(constraint_dict, table_name=''):
    """
    查询一条记录
    :param constraint_dict:约束条件字典
    :param table_name: 表名，不填则为默认表
    :return:列表
    """
    key = list(constraint_dict.keys())[0]
    value = list(constraint_dict.values())[0]
    select_key = eval('query.{}==\'{}\''.format(key, value))
    if table_name == '':
        results = list(db.search(select_key))
    else:
        results = list(db.search(select_key, table=table_name))
    return results


def table(table_name=''):
    """
    返回一张表所有的内容
    :param table_name:表名
    :return: 列表
    """
    return list(db.all()) if table_name == '' else list(db.all(table_name))


def del_data(data_dict, table_name=''):
    """
    删除一条数据
    :param table_name:
    :param data_dict:
    :return:
    """
    if table_name == '':
        db.delete(data_dict)
    else:
        db.delete(data_dict, table=table_name)


def create_table(key_list, table_name):
    """
    创建一张表
    :param key_list: [键，键，键……]
    :param table_name: 表名
    :return:
    """
    db.create_table(key_list, table_name)


def del_table(table_name):
    """
    删除一张表
    :param table_name:
    :return:
    """
    db.purge(table_name)


def has_url(url, table_name=''):
    """
    在一张表中查询url是否存在
    :param url:
    :param table_name:
    :return:
    """
    dict_ = {'url': url}
    if table_name != '':
        return db.exist(dict_, table_name)
    else:
        return db.exist(dict_)
