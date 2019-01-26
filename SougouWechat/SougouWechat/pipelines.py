# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from pandas.tests.extension.base import getitem
import pymysql
import SougouWechat.settings as settings


# 将不同item插入对应MySQL表的pipeline类
class MySQLPipeline(object):
    
    def __init__(self):
        #self.sql_dict = {'gzh_info_item':'insert ignore into wechat_info(wechat_id, wechat_name, introduction, authentication, headimage, open_id, qrcode, post_perm, view_perm, profile_url, origin_url) VALUES(%s,%s,%s,%s,%s,%s,%s,%d,%d,%s,%s);'}
        self.sql_dict = {'wechat_to_crawl':['no','name','link_url','refer_url','category','is_crawled'],
                         'wechat_info':['wechat_id','wechat_name','introduction','authentication','headimage','open_id','qrcode','post_perm','view_perm','profile_url','origin_url','update_datetime']}
        self.item_dict = {'wechat_to_crawl':[],
                          'wechat_info':[]
                          }
        self.bulk_size = 100
        self.logger = logging.getLogger()
        
    def sql_generator(self, item):
        try:
            sql = ''
            sql = 'insert ignore into %s' % item['table_name']
            sql = sql + "(" +  ", ".join(self.sql_dict[item['table_name']]) 
            sql = sql +  ") VALUES(%s);" %('%s,'*(len(self.sql_dict[item['table_name']])-1) + '%s')
        except Exception as e:
            self.logger.exception(e)        
        finally:
            return sql
    
    def insert_all_items(self):
        for key in self.sql_dict:
            if len(self.item_dict[key]) > 0:
                try:
                    sql = 'insert ignore into %s' % key
                    sql = sql + "(" +  ", ".join(self.sql_dict[key]) 
                    sql = sql +  ") VALUES(%s);" %('%s,'*(len(self.sql_dict[key])-1) + '%s')
                    try:
                        self.cursor.executemany(sql, self.item_dict[key])
                        self.connect.commit()
                    except Exception as e:
                        self.connect.rollback()
                        self.logger.exception(e)                        
                except Exception as e:
                    self.logger.exception(e)                 
    
    def insert_items(self, item):
        try:
            sql = self.sql_generator(item)
            self.cursor.executemany(sql, self.item_dict[item['table_name']])
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            self.logger.exception(e)
    
    def process_item(self, item, spider):
        try:
            item_list = []
            for each in self.sql_dict[item['table_name']]:
                item_list.append(item[each])
            print(item_list)
            self.item_dict[item['table_name']].append(item_list)
            if len(self.item_dict[item['table_name']]) >= self.bulk_size:
                 self.insert_items(item)
                 del self.item_dict[item['table_name']][:]
        except Exception as e:
            self.logger.exception(e)
        finally:                
            return item
    
    def open_spider(self, spider):
        try:
            self.connect = pymysql.connect(
                host=settings.MYSQL_HOST,
                db=settings.MYSQL_DBNAME,
                user=settings.MYSQL_USER,
                passwd=settings.MYSQL_PASSWD,
                charset='utf8mb4',
                use_unicode=True)
            self.cursor = self.connect.cursor()
        except Exception as e:
            self.logger.exception(e)
    
    def close_spider(self, spider):
        try:
            self.insert_all_items()
        except Exception as e:
            self.logger.exception(e)
        finally:
            self.cursor.close()
            self.connect.close()
        
