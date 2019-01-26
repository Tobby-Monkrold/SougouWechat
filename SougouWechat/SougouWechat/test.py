# -*- coding:utf-8 -*-
import scrapy
import wechatsogou
import json
from lxml import etree
from rk_client import RClient
import settings
import traceback
import requests
import pymysql
import time

class WechatSpider(object):
    
    def __init__(self):
        self.start_urls = []
        self.wechat_infos = []
        self.result_id = ""
        start_url = "http://top.anyv.net/"
        self.parse_category(start_url)
        username = settings.username
        password = settings.password
        id_ = settings.id
        key = settings.key
        self.rc = RClient(username, password, id_, key)        
        
        
        
    def identify_image_callback(self, img, code="3060"):
        try:
            username = settings.username
            password = settings.password
            id_ = settings.id
            key = settings.key
            rc = RClient(username, password, id_, key)
            result = rc.rk_create(img, code)
            self.result_id = result['Id']
            print('验证码：', result['Result'])
            return result['Result']
        except Exception as e:
            print(traceback.format_exc())
            
    def parse_category(self, start_url):
        try:
            response = requests.get(start_url)
            r = etree.HTML(response.text, etree.HTMLParser(encoding='utf-8'))
            for grid in r.xpath('/html/body/div[3]/div/div/ul/li[@class="grid"]'):
                url = grid.xpath('a/@href')[0]
                self.start_urls.append(url)
            print("category parsed already")
        except Exception as e:
            print(traceback.format_exc())   
                     
    def parse_url(self, url):
        print(url)
        try:
            response = requests.get(url)
            r = etree.HTML(response.text, etree.HTMLParser(encoding='utf-8'))
            for item in r.xpath('/html/body/div[4]/div[1]/div[5]/ul/div[@class="newpicsmall_list"]'):
                url = item.xpath('a/@href')[0]
                name = item.xpath('a/li[@class="xiaobiaotizi"]/text()')
                if len(name) == 0:
                    continue
                name = name[0]
                print(name,url)
                ws_api = wechatsogou.WechatSogouAPI()
                try:
                    wechat_info = ws_api.get_gzh_info(name, identify_image_callback=self.identify_image_callback)
                except wechatsogou.exceptions.WechatSogouVcodeOcrException as e:
                    result = rc.rk_report_error(self.result_id)
                    print("验证码错误,报错上传：", result["Result"])
                    continue
                if wechat_info is not None:
                    item = []
                    item.append(wechat_info['wechat_id']) # 微信公众号名称
                    item.append(wechat_info['wechat_name']) # 微信公众号id
                    item.append(wechat_info['introduction']) # 简介
                    item.append(wechat_info['authentication']) #认证
                    item.append(wechat_info['headimage']) #头像url
                    item.append(wechat_info['open_id']) 
                    item.append(wechat_info['qrcode']) # 二维码
                    item.append(int(wechat_info['post_perm'])) # 最近一月群发量
                    item.append(int(wechat_info['view_perm'])) # 最近一月阅读数
                    item.append(wechat_info['profile_url']) # 最近10条群发页链接
                    item.append(url) # 原始url
                    item.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    self.wechat_infos.append(item)
                    self.insert_to_mysql()
            nextpage = r.xpath('//*[@id="content-pagenation"]/div/div/div/a[@class="next"]/@href')[0]
            if len(nextpage) > 0:
                self.parse_url(nextpage)
        except Exception as e :
            print(traceback.format_exc())
            

    def insert_to_mysql(self):
        if len(self.wechat_infos) >= 2:
            self.exceute_sql()
            self.wechat_infos = []
    
    def exceute_sql(self):
        try:
            connect = pymysql.connect(
                host=settings.MYSQL_HOST,
                db=settings.MYSQL_DBNAME,
                user=settings.MYSQL_USER,
                passwd=settings.MYSQL_PASSWD,
                charset='utf8',
                use_unicode=True)
            cursor = connect.cursor()
            sql = 'insert ignore into wechat_info(wechat_id, wechat_name, introduction, authentication, headimage, open_id, qrcode, post_perm, view_perm, profile_url, origin_url, update_datetime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
            #print(self.wechat_infos)
            cursor.executemany(sql, self.wechat_infos)
            connect.commit()
        except Exception as e:
            print(traceback.format_exc())
        finally:
            cursor.close()
            connect.close()

spider = WechatSpider()
spider.parse_url(spider)


