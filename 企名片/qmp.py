# -*- coding: utf-8 -*- 
# @email : upapqqxyz@gmail.com
# @Author : Ane
import requests
import execjs
import json
def getEncryptData():
    url="https://vipapi.qimingpian.cn/DataList/productListVip"
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0"}
    EncryptData=requests.post(url=url,headers=headers).json()["encrypt_data"]
    return EncryptData

if __name__ == '__main__':
    data=getEncryptData()
    with open("encrypt.js","r",encoding="utf8") as file:
        jscode=file.read()
    js=execjs.compile(jscode)
    res=js.call("o",data)
    datalist=json.loads(res)
    print(datalist)