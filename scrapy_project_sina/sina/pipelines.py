# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
from items import zongyiItem, ChinaItem, filmItem
from SQLmodel import data, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine



class SinaPipeline(object):
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://root:200683088@localhost:3306/sina',encoding='utf-8')
        Base.metadata.create_all(self.engine)
        self.DBSession = sessionmaker(bind=self.engine)

    def process_item(self, item, spider):
        if item['category']=='zongyi':
            with open('./data/zongyi.csv','a+',encoding='utf-8',newline='') as f:
                writer = csv.writer(f,delimiter='\t')
                print('----------------------check-----------------')
                print(item['title'],item['time_stamp'], item['article'])
                print('--------------------------------------------')
                writer.writerow((item['title'],item['time_stamp'],item['article']))
        
        if item['category']=='China':
            with open('./data/china.csv','a+',encoding='utf-8',newline='') as f:
                writer = csv.writer(f, delimiter='\t')
                print('----------------------check-----------------')
                print(item['title'],item['time_stamp'], item['article'])
                print('--------------------------------------------')
                writer.writerow((item['title'],item['time_stamp'],item['article']))
        
        if item['category']=='film':
            with open('./data/film.csv','a+',encoding='utf-8',newline='') as f:
                writer = csv.writer(f,delimiter='\t')
                print('----------------------check-----------------')
                try:
                    print(item['title'],item['time_stamp'], item['article'])
                except:
                    print(item['title'],item['time_stamp'],item['pagetype'],item['category'])
                    print(type(item['article']))
                print('--------------------------------------------')
                writer.writerow((item['title'],item['time_stamp'],item['article']))
        new = data()
        new.title = item['title']
        try:
            new.article = item['article']
        except:
            print(item['title'],item['category'],item['time_stamp'])
            print(item['pagetype'])
            print(item['article'])
        new.category = item['category']
        new.time_stamp = item['time_stamp']
        new.pagetype = item['pagetype']
        session = self.DBSession()
        session.add(new)
        session.commit()
        return item
