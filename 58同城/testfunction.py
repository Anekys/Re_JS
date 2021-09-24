# -*- coding: utf-8 -*- 
# @email : upapqqxyz@gmail.com
# @Author : Ane
from fontTools.ttLib import TTFont
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO
import requests
import base64
from lxml import etree
import numpy
def fontConvert(fontPath):     #将web下载的字体文件解析，返回其编码和汉字的对应关系
    font = TTFont(fontPath)  # 打开文件
    codeList = font.getGlyphOrder()[1:-1]
    im = Image.new("RGB", (1600, 50), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(fontPath,40)
    # count = 1
    # arrayList = numpy.array_split(codeList,count)   #将列表切分，
    # for t in range(count):
    #     # print(arrayList[t])
    #     # print(t)
    #     newList = [i.replace("uni", "\\u") for i in arrayList[t]]
    #     text = "".join(newList)
    #     text = text.encode('utf-8').decode('unicode_escape')
    #     dr.text((0, 50*t), text, font=font, fill="#000000")
    newList=[i.replace("uni", "\\u") for i in codeList]
    text = "".join(newList)
    text = text.encode('utf-8').decode('unicode_escape')
    dr.text((0,0), text, font=font, fill="#000000")
    # img_byte=BytesIO()
    # im.save(img_byte,format='png')
    # binary_str2 = img_byte.getvalue()
    # with open("test.png","wb") as f:
    #     f.write(binary_str2)
    im.save("sss.jpg")
    # return img_byte.getvalue()
    # im = Image.open("sss.jpg")      #可以将图片保存到本地，以便于手动打开图片查看
def ocr(image):
    apikey="wiPp17RqG7LNPiZoU5d9AgRx"
    secretkey="449Ie4au6zipvpXsanT4bNCnFcI1GAEc"
    host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={apikey}&client_secret={secretkey}'
    try:
        token=requests.get(host).json()['access_token']
    except:
        token = requests.get(host).json()
        print(token)
        return
    img=base64.b64encode(image)
    params = {"image": img}
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    res=requests.post(url="https://aip.baidubce.com/rest/2.0/ocr/v1/form?access_token="+token,headers=headers,data=params).json()
    words=res["forms_result"][0]["header"][0]["words"]
    wordlist=[i for i in words]
    print(wordlist)

def getinfo(html):
    tree=etree.HTML(html)
    infolist=[]
    dl=tree.xpath("/html/body/div[5]/div[2]/div[2]/dl")
    for dt in dl:
        info = {}
        info["qzyx"]=dt.xpath("./dt/a/text()")[0]
        info["xb"]=dt.xpath("./dd[3]/text()")[0]
        info["nl"]=dt.xpath("./dd[4]/text()")[0]
        info["gzjy"]=dt.xpath("./dd[5]/text()")
        info["xl"]=dt.xpath("./dd[6]/text()")[0]
        info["mqzw"]=dt.xpath("./dd[7]/text()")[0]
        info["hysj"]=dt.xpath("./dd[8]/span[1]/text()")
        infolist.append(info)
    return infolist

with open("test.html","r",encoding="utf-8") as f:
    html=f.read()
print(html)
list=getinfo(html)
for i in list:
    print(i)