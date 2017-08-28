
def is_has_dict(key,_dict):
    t1 = time.time()
    _is_has = False
    for d in _dict:
        if str(key) == str( d['uid'] ):
            return True
        else :
            continue
    return _is_has