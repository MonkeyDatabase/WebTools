import hashlib


def gen_md5(raw_code:bytes):
    MD5 = hashlib.md5()
    MD5.update(raw_code)
    return MD5.hexdigest()
