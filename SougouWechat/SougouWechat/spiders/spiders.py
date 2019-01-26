# -*- coding:utf-8 -*-
import scrapy
from SougouWechat.items import WechatNameItem
import logging


class WechatNameSpider(scrapy.spiders.Spider):
    name = 'WechatNameSpider'
    start_urls = ["http://top.anyv.net/"]
    item_count = 0
    logger = logging.getLogger()
    
    # 获取category的url
    def parse(self, response):
        try:
            # 遍历category
            for grid in response.xpath('/html/body/div[3]/div/div/ul/li[@class="grid"]'):
                url = grid.xpath('a/@href').extract()[0]
                category = grid.xpath('a/text()').extract()[0]
                yield scrapy.Request(url, callback=self.parse_url, meta={'category':category})
        except Exception as e:
            self.logger.exception(e)
        
        # yield scrapy.Request("http://www.anyv.net/index.php/category-1", callback=self.parse_url)
    
    # 获取公众号名称        
    def parse_url(self, response):
        try:
            for item in response.xpath('/html/body/div[4]/div[1]/div[5]/ul/div[@class="newpicsmall_list"]'):
                link_url = item.xpath('a/@href').extract()[0]
    
                name = item.xpath('a/li[@class="xiaobiaotizi"]/text()').extract()
                if len(name) == 0:
                    continue
                else:
                    name = name[0]
                    
                category = response.meta['category']
                self.item_count = self.item_count + 1
                refer_url = response.url
                
                # 数据填充入item中
                mysql_item = WechatNameItem()
                mysql_item['table_name'] = "wechat_to_crawl" # 表名称,用于pipeline识别
                mysql_item['no'] = self.item_count # no,主键
                mysql_item['name'] = name # 公众号名称，可能不存在或错误
                mysql_item['link_url'] = link_url # 公众号主页
                mysql_item['refer_url'] = refer_url # category链接
                mysql_item['category'] = category # category名称
                mysql_item['is_crawled'] = "False" # 是否已爬虫解析
                yield mysql_item
                
                # 解析下一页 
                nextpage = response.xpath('//*[@id="content-pagenation"]/div/div/div/a[@class="next"]/@href').extract()
                if len(nextpage) > 0:
                    yield scrapy.Request(nextpage[0], callback = self.parse_url, meta={'category':category})
                
        except Exception as e:
            self.logger.exception(e)
            

class WechatInfoSpider(scrapy.spiders.Spider):    
    name = "WechatInfoSpider"
    start_urls = []
    logger = logging.getLogger()
    
    def parse(self, response):
        pass
    
    
        
        
        
        
        
        
        
        