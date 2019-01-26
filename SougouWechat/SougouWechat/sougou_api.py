# -*- coding:utf-8 -*-
import logging
import os
import requests
import json
from lxml import etree
from rk_client import RClient
import io
from PIL import Image
import settings

logging.basicConfig(level=logging.WARNING,
                    filename='log.txt', 
                    filemode='w', 
                    format='%(asctime)s - %(filename)s[line:%>(lineno)d] - %(levelname)s: %(funcName)s | %(message)s')

class SougouApi(object):
    
    # 初始化
    def __init__(self, cookies_file_path=None):    
        try:
            # 初始化默认headers
            self.headers = {"Host": "weixin.sogou.com",
                        "Connection": "keep-alive",
                       "Upgrade-Insecure-Requests": "1",
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                       "Referer": "https://weixin.sogou.com/weixin?type=1&s_from=input&query=%E5%A0%A1%E5%9E%92%E4%B9%8B%E5%A4%9C%E5%A4%A7%E8%AE%B2%E5%A0%82&ie=utf8&_sug_=n&_sug_type_=",
                       "Accept-Encoding": "gzip, deflate, br",
                       "Accept-Language": "zh-CN,zh;q=0.9"
                       }
            
            # 初始化params参数
            self.params = {"type": "1",
                           "query": "",
                           "ie": "utf8",
                           "s_from": "input",
                           "_sug_": "y",
                           "_sug_type_": "",
                           "w": "01019900",
                           "sut": "1810",
                           "sst0": "1548383817768",
                           "lkt": "0,0,0"}
                
            # 读取cookies文件
            if cookies_file_path != None:
                with open(path,'r') as f:
                    listCookie = json.loads(f.read())
                self.cookies = {}
                for cookie in listCookie:
                    self.cookies[cookie["name"]] = cookie["value"]
            else:
                self.cookies = {"Cookie":"weixinIndexVisited=1; ABTEST=8|1548383402|v1; SNUID=C9A203413135B10E2A97D1EE3139BBA1; IPLOC=CN3504; SUID=F89232704842910A000000005C4A74AA; JSESSIONID=aaawZ24YzcJPS8IazN5Hw; SUID=F89232703020910A000000005C4A74AC; SUV=00201C77703292F85C4A755AC3A38031; sct=1"}
        except Exception as e:
            logging.exception(e)
    
    # 设置默认cookies
    def set_default_cookies(self, cookies):
        self.default_cookies = cookies

    # 设置默认headers
    def set_default_headers(self, headers):
        self.headers = headers
    
    # 设置params参数
    def set_params(self, params):
        self.params = params
    
    # 获取公众号信息    
    def get_gzh_info(self, query):
        try:
            self.params['query'] = query
            response = requests.get("https://weixin.sogou.com/weixin", cookies=cookies, params=params,headers=headers,verify=False)
            if response.status_code == 200:
                url_quote = response.url
                res_etree = etree.HTML(response.text, etree.HTMLParser(encoding='utf-8'))
                # 检查是否出现验证码
                src = res_etree.xpath('//*[@id="seccodeImage"]/@src')
                if len(src) > 0:
                    self.unlock_code(src[0])
                else:
                    self.parse_gzh_page(res_etree)
        except Exception as e:
            logging.exception(e)

    # 识别验证码
    def unlock_code(self, src):
        try:
            url = "https://weixin.sogou.com/antispider/" + src
            response = requests.get(url, cookies=cookies, params=params,headers=headers,verify=False)
            rc_username = settings.username
            rc_password = settings.password
            rc_id = settings.id
            rc_key = settings.key
            rc = RClient(rc_username, rc_password, rc_id, rc_key)
            result = rc.rk_create(response.content, "3000")
            
            return result
            
        except Exception as e:
            logging.exception(e)
        finally:
            return result
        
    # 解析公众号查询页面信息
    def parse_gzh_page(self, res_etree):
        pass











path = r"D:/Eclipse/eclipse-java-oxygen-1a-win32-x86_64/eclipse/workspace/SougouWechat/SougouWechat/cookies.txt"

with open(path,'r') as f:
    listCookie = json.loads(f.read())

cookies = {}

for cookie in listCookie:
    cookies[cookie["name"]] = cookie["value"]

params = {"type": "1",
          "query": "堡垒之夜",
          "ie": "utf8",
          "s_from": "input",
          "_sug_": "y",
          "_sug_type_": "",
          "w": "01019900",
          "sut": "1810",
          "sst0": "1548383817768",
          "lkt": "0,0,0"}

#cookies = {"Cookie":"weixinIndexVisited=1; ABTEST=8|1548383402|v1; SNUID=C9A203413135B10E2A97D1EE3139BBA1; IPLOC=CN3504; SUID=F89232704842910A000000005C4A74AA; JSESSIONID=aaawZ24YzcJPS8IazN5Hw; SUID=F89232703020910A000000005C4A74AC; SUV=00201C77703292F85C4A755AC3A38031; sct=5"}

headers = {"Host": "weixin.sogou.com",
"Connection": "keep-alive",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"Referer": "https://weixin.sogou.com/weixin?type=1&s_from=input&query=%E5%A0%A1%E5%9E%92%E4%B9%8B%E5%A4%9C%E5%A4%A7%E8%AE%B2%E5%A0%82&ie=utf8&_sug_=n&_sug_type_=",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9"
}

src = []
while len(src)==0:
    response = requests.get("https://weixin.sogou.com/weixin", cookies=cookies, params=params,headers=headers,verify=False)
    url_quote = response.url
    r = etree.HTML(response.text, etree.HTMLParser(encoding='utf-8'))
    src = r.xpath('//*[@id="seccodeImage"]/@src')
    print(src)

src = src[0]

print(src)

print(cookies)

url = "https://weixin.sogou.com/antispider/" + src

response = requests.get(url, cookies=cookies, params=params,headers=headers,verify=False)
byte_stream = io.BytesIO(response.content)
img = Image.open(byte_stream)
rc = RClient("twenty1997", "qwertyuiop", "121594", '4078ac6237be405fbdf9ecf5476cfdc0')


with open("code.jpg", "wb") as f:
    f.write(response.content)
    print("ok")

result = rc.rk_create(response.content, "3000")
print(result)
print('验证码：', result['Result'])
print(img.info)
url_quote = url_quote.split('weixin.sogou.com/')[-1]
data = {
    'c': result['Result'],
    'r': '%2F' + url_quote,
    'v': 5    
    }
res = requests.post("https://weixin.sogou.com/antispider/thank.php", cookies=cookies, data=data,headers=headers,verify=False)
print(res.content.decode("utf-8"))
cookies["refresh"] = "1"
cookies["seccodeRight"] = "success"
res = requests.get("https://weixin.sogou.com/weixin", cookies=cookies, params=params,headers=headers,verify=False)
print(res.content.decode("utf-8"))
#print(response.content.decode("utf-8"))









