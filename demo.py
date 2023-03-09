"""
    hashlib 加密
"""
import getpass
import hashlib

pwd = getpass.getpass()
print(pwd)

# 加密处理
hash = hashlib.md5()
hash.update(pwd.encode())
pwd = hash.hexdigest()
print(pwd)
