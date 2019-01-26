# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class WechatInfoItem(scrapy.Item):
    table_name = scrapy.Field() # 表名称,用于pipeline识别
    wechat_name = scrapy.Field() # 微信公众号名称
    wechat_id = scrapy.Field() # 微信公众号id
    introduction = scrapy.Field() # 简介
    authentication = scrapy.Field() #认证
    headimage = scrapy.Field() #头像url
    open_id = scrapy.Field() 
    qrcode = scrapy.Field() # 二维码
    post_perm = scrapy.Field() # 最近一月群发量
    view_perm = scrapy.Field() # 最近一月阅读数
    profile_url = scrapy.Field() # 最近10条群发页链接
    origin_url = scrapy.Field() # 原始url
    
class WechatNameItem(scrapy.Item):
    table_name = scrapy.Field() # 表名称,用于pipeline识别
    no = scrapy.Field() # no,主键
    name = scrapy.Field() # 公众号名称，可能不存在或错误
    link_url = scrapy.Field() # 公众号主页
    refer_url = scrapy.Field() # category链接
    category = scrapy.Field() # category名称
    is_crawled = scrapy.Field() # 是否已爬虫解析
    
    
