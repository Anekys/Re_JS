# -*- coding: utf-8 -*- 
# @email : upapqqxyz@gmail.com
# @Author : Ane
import requests
import execjs
def GenerateSign(word):
    with open("sign.js","r",encoding="utf8") as file:
        jscode=file.read()
    js=execjs.compile(jscode)
    sign=js.call("e",word)
    return sign
def getdate(word):
    url="https://fanyi.baidu.com/v2transapi?from=en&to=zh"
    headers={
        'Cookie': 'BAIDUID=438EDC74FDED27C89A1E7B2FE7EC9316:FG=1',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    formdata={
        "from": "en",
        "to": "zh",
        "query": word,
        "transtype": "realtime",
        "simple_means_flag": "3",
        "sign": GenerateSign(word),
        "token": "101593b573c90b330d684e94133a5cd0",
        "domain": "common"
    }
    res=requests.post(url=url,headers=headers,data=formdata).json()
    print(res)
if __name__ == '__main__':
    getdate("dog")