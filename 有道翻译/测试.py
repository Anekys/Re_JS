# -*- coding: utf-8 -*- 
# @email : upapqqxyz@gmail.com
# @Author : Ane
import requests
import random
import time
from hashlib import md5
def run(text):
    url="https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
    headers={
        "Cookie": 'OUTFOX_SEARCH_USER_ID=-439837580@10.169.0.83; OUTFOX_SEARCH_USER_ID_NCOO=986990596.0994844; fanyi-ad-id=114757; fanyi-ad-closed=1; JSESSIONID=aaaUyRqw9jBFh4UwlfiUx; ___rl__test__cookies=1630076227298',
        "Referer": 'https://fanyi.youdao.com/',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4621.4 Safari/537.36'
    }
    lts=get_lts()
    salt=get_salt(lts)
    sign=get_sign(text,salt)
    data = {
        "i": text,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": salt,
        "sign": sign,
        "lts": lts,
        "bv": "c494f72cba54a5d5ec07a78b3a85e4c8",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        'action': 'FY_BY_REALTlME',
    }
    res=requests.post(url=url,headers=headers,data=data).text
    print(res)

def get_lts():
    lts=str(int(time.time()*1000))
    return lts
def get_salt(lts):
    salt = lts + str(random.randint(0, 9))
    return salt
def get_sign(text,salt):
    s=md5()
    s = md5()
    sign = "fanyideskweb" + text + salt + "Y2FYu%TNSbMCxc3t2u^XT"
    s.update(sign.encode())
    sign = s.hexdigest()
    return sign
if __name__ == '__main__':
    run("english")