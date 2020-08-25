# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#def save2csv(title, article, time_stamp, category):
#    if category=="China":
#        if os.path.exists('../raw_data/china.csv'):
#            f = open('../raw_data/china.csv')


class ChinaItem(scrapy.Item):
    title = scrapy.Field()
    article = scrapy.Field()
    time_stamp = scrapy.Field()
    category = scrapy.Field()

class zongyiItem(scrapy.Item):
    title = scrapy.Field()
    article = scrapy.Field()
    time_stamp = scrapy.Field()
    category = scrapy.Field()

class filmItem(scrapy.Item):
    title = scrapy.Field()
    article = scrapy.Field()
    time_stamp = scrapy.Field()
    category = scrapy.Field()

class dataItem(scrapy.Item):
    title = scrapy.Field()
    article = scrapy.Field()
    time_stamp = scrapy.Field()
    category = scrapy.Field()
    pagetype = scrapy.Field()