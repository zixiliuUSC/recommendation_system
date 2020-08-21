# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
from items import zongyiItem, ChinaItem, filmItem
class SinaPipeline(object):
    def process_item(self, item, spider):
        if item.__class__==zongyiItem:
            with open('./data/zongyi.csv','a+',encoding='utf-8',newline='') as f:
                writer = csv.writer(f,delimiter='\t')
                print('----------------------check-----------------')
                print(item['title'],item['time_stamp'], item['article'])
                print('--------------------------------------------')
                writer.writerow((item['title'],item['time_stamp'],item['article']))
        
        if item.__class__==ChinaItem:
            with open('./data/china.csv','a+',encoding='utf-8',newline='') as f:
                writer = csv.writer(f, delimiter='\t')
                print('----------------------check-----------------')
                print(item['title'],item['time_stamp'], item['article'])
                print('--------------------------------------------')
                writer.writerow((item['title'],item['time_stamp'],item['article']))
        
        if item.__class__==filmItem:
            with open('./data/film.csv','a+',encoding='utf-8',newline='') as f:
                writer = csv.writer(f,delimiter='\t')
                print('----------------------check-----------------')
                print(item['title'],item['time_stamp'], item['article'])
                print('--------------------------------------------')
                writer.writerow((item['title'],item['time_stamp'],item['article']))
        return item
