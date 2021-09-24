# -*- coding: utf-8 -*- 
# @email : upapqqxyz@gmail.com
# @Author : Ane
import requests
from fontTools.ttLib import TTFont
import re
import base64
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO
from lxml import etree
def gethtml():      #获取网页HTML源码
    url = "https://bj.58.com/searchjob/pn1/"
    Cookie = """f=n;commontopbar_new_city_info=4%7C%E6%B7%B1%E5%9C%B3%7Csz;f=n;commontopbar_new_city_info=4%7C%E6%B7%B1%E5%9C%B3%7Csz;commontopbar_ipcity=sanhe%7C%E4%B8%89%E6%B2%B3%7C0;58home=bj;id58=c5/nfGE4P3tDjwYSA3k1Ag==;city=sanhe;58tj_uuid=7f7d4c45-27ff-4a47-9204-03ae29e5fc8d;new_uv=3;als=0;wmda_uuid=c088765f8ad0c9ceed1e133b43230201;wmda_new_uuid=1;wmda_visited_projects=%3B11187958619315%3B1731916484865%3B10104579731767;xxzl_deviceid=41RpNlQsKM9muuq36FbRvEM5a6IFzpBNRjnNvW%2FJWD5wBjdYPyo5lCrcL4j8ER8L;fzq_h=0107875ee654736b966819466034a1ed_1631076244014_a23c44d2f5804812a359467b2818bad7_1007338212;param8616=1;param8716kop=1;PPU="UID=56572755967758&UN=23ze5bdx9&TT=be892a92bd8228e4621bd4810a99731b&PBODY=F82r0htebPWy51dEx6U989OQxEc_1g8SngF6-y-qvjhbhJ6gbF8A9KNiW9onbtDGCyf8j73tHhlEhlJEAigSoSJDowHgouj6lMPSnJ5LEfpmUNUhuyO4NAo0k5A0R0t72isHGA3A1hlI_72N2sFnqcfooYQ-OQ_QISz8wnbUACI&VER=1&CUID=HrD8pv77g3TioovXZymtTA";58uname=23ze5bdx9;passportAccount="atype=0&bstate=0";jl_list_left_banner=14;xxzl_smartid=fe503117518a61bfc16bc0a49ed84fae;isSmartSortTipShowed=true;ljrzfc=1;isShowProtectTel=true;sessionid=70ce3232-f5d6-4704-99ab-c89f1aaf9306;JSESSIONID=C6E2E5B7EAB053823AC93E63617A1B17;f=n;new_session=0;utm_source=;spm=;init_refer=;wmda_session_id_1731916484865=1631096191690-93d91732-63e5-9843;xxzl_cid=1e341892f62644b5a4843b7c667766c1;xzuid=e0780ff6-51b7-46c3-8b3a-980de4132f2b"""
    header = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "Cookie": Cookie
    }
    res = requests.get(url, headers=header).text
    return res
def parfontfile(html):      #解析源码中的字体库并保存为font.woff
    b64=re.compile("base64,(.*)\)") #匹配字体文件的base64编码
    b64str=re.findall(b64,html)[0]
    try:
        b64file = base64.decodebytes(b64str)
    except:
        b64file = b64decode(b64str)
    with open("font.woff","wb") as file:
        file.write(b64file)
def b64decode(origStr):     #base64解码防错误填充版
    #base64 decode should meet the padding rules
    if(len(origStr)%3 == 1):
        origStr += "=="
    elif(len(origStr)%3 == 2):
        origStr += "="
    origStr = bytes(origStr, encoding='utf8')
    dStr = base64.decodebytes(origStr)
    return dStr
def font_to_xml():      #将字体文件转换为xml文件,方便查看
    fonts=TTFont("font.woff")
    fonts.saveXML("font.xml")
def font2png(fontPath):     #将字体文件转换为图片,参数为字体文件的路径,返回文件字节流,及字符UnicodeNames
    font = TTFont(fontPath)
    glyphnames = font.getGlyphNames()[1:]
    if glyphnames[len(glyphnames) - 1] == "x":
        glyphnames = glyphnames[:-1]
    elif glyphnames[0] == "x":
        glyphnames = glyphnames[1:]
    im = Image.new("RGB", (1600, 50), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(fontPath,40)
    newList = [i.replace("uni", "\\u") for i in glyphnames]
    text = "".join(newList)
    text = text.encode('utf-8').decode('unicode_escape')
    dr.text((0, 0), text, font=font, fill="#000000")
    img_byte=BytesIO()
    im.save(img_byte,format='png')
    return img_byte.getvalue(),glyphnames

def ocr(image):     #利用百度OCR的API识别图片中的文字,参数为图片字节流,返回识别到的文字列表,每个元素为一个字
    apikey="你的APIkey"
    secretkey="你的SecretKey"
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
    return wordlist

def getinfo(html):
    tree=etree.HTML(html)
    infolist=[]
    dl=tree.xpath("/html/body/div[5]/div[2]/div[2]/dl")
    for dt in dl:
        info = {}
        info["求职意向"]=dt.xpath("./dt/a/text()")[0]
        info["性别"]=dt.xpath("./dd[3]/text()")[0]
        info["年龄"]=dt.xpath("./dd[4]/text()")[0]
        info["工作经验"]=dt.xpath("./dd[5]/text()")[0]
        info["学历"]=dt.xpath("./dd[6]/text()")[0]
        info["目前职位"]=dt.xpath("./dd[7]/text()")[0]
        info["活跃时间"]=dt.xpath("./dd[8]/span[1]/text()")[0]
        infolist.append(info)
    return infolist
if __name__ == '__main__':
    html=gethtml()
    print(html)
    parfontfile(html)
    font_to_xml()
    img,glyphnames=font2png("font.woff")
    def zhuanhuan(string):
        string = "&#x" + string[3:].lower() + ";"
        return string
    Glyphnames=[zhuanhuan(i) for i in glyphnames]
    wordlist=ocr(img)
    if wordlist != None:
        font_map=dict(zip(Glyphnames,wordlist))
        for key in font_map:
            html=html.replace(key,font_map[key])
        with open("test.html","w",encoding="utf-8") as file:
            file.write(html)
        info=getinfo(html)
        for i in info:
            print(i)
    else:
        print("ocr识别失败,程序结束")