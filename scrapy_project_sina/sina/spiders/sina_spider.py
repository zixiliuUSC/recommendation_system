# -*- coding: utf-8 -*-
import scrapy
import selenium
from selenium import webdriver
from scrapy.http import Request
from sina.items import *
from scrapy import Selector
import os
import pandas as pd
import unicodedata
from bs4 import BeautifulSoup


import datetime
import re
import sys

class SinaSpiderSpider(scrapy.Spider):

    name = 'sina_spider'
    allowed_domains = ['sina.com.cn']
    
    def __init__(self, page=None, flag=None, *args, **kwargs):
        super(SinaSpiderSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://news.sina.com.cn/china/',
                    'https://ent.sina.com.cn/zongyi/',
                    'https://ent.sina.com.cn/film/']
        self.options = webdriver.ChromeOptions() # ChromeOptions是用来配置Chrome浏览器的特性，可以配置的选项见网页：https://peter.sh/experiments/chromium-command-line-switches/
        self.options.add_argument('headless')
        self.options.add_argument('no-sandbox')
        self.options.add_argument('--blink-setting=imagesEnabled=false')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--disable-javascript')
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_argument('--disable-plugins')
        self.options.add_experimental_option('prefs',{ 'profile.default_content_setting_values': { 'notifications' : 2 }})

        #self.directory = "M:\\scrapy_project\\recommendation_system\\scrapy_project_sina\\data"
        self.page = int(page) # 目前是不合理的，要从外面传进来
        self.flag = int(flag) # 暂时定义这个变量，后面会用到


    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)
            #break


    def parse(self, response):
        #self.logger.info(response.text)
        driver = webdriver.Chrome(chrome_options=self.options)
        driver.set_page_load_timeout(100)
        driver.get(response.url)
        now = datetime.datetime.now()
        pagetype = None
        stamp1 = now.replace(hour=0,minute=0,second=0)
        stamp2 = now.replace(hour=12,minute=0,second=0)
        stamp3 = now.replace(day=now.day-1,hour=12,minute=0,second=0)
        if self.flag == 1:
            self.page = 100
        for i in range(self.page):
        #while (self.page>0):
            while not driver.find_element_by_xpath("//div[@class='feed-card-page']").text:
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);") # selenium的driver类可以用execute_script()函数在浏览器内部执行JavaScript。
            count = driver.find_elements_by_xpath("//div[@class='feed-card-item']")
            for each in count:
                htmltext = each.get_attribute('innerHTML')
                soup = BeautifulSoup(htmltext, 'html5lib')
                time = soup.find('div', {'class':"feed-card-time"}).contents[0]
                temp = soup.find('h2').contents[0]
                href = temp.attrs['href']
                title = temp.contents[0]
                item = dataItem()
                item['title'] = unicodedata.normalize('NFKC',title)
                title = temp.contents[0]
                if '/video' in href:
                    pagetype = 'video'
                elif '/slide' in href:
                    pagetype = 'img'
                elif '/doc' in href:
                    pagetype = 'doc'
                if response.url == "https://ent.sina.com.cn/zongyi/":
                    #item = zongyiItem()
                    item['category'] = 'zongyi'
                elif response.url == "https://news.sina.com.cn/china/":
                    #item = ChinaItem()
                    item['category'] = 'China'
                else:
                    #item = filmItem()
                    item['category'] = 'film'

                # parse time_stamp for current link
                if "分钟前" in time:
                    continue  # 因为n分钟前求出的新闻时间并不准确，所以不作处理
                elif "今天" in time:
                    hour, minute = map(int, re.findall(r"[0-9]+", time))
                    time = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=hour, minute=minute)
                else:
                    month, day, hour, minute = map(int, map(str.strip, re.split(r"[月日:]", time)))
                    time = datetime.datetime(year=now.year, month=month, day=day, hour=hour, minute=minute)

                if self.flag==1: # flag==1, do update crawling
                    # decide whether to yield or stop crawling according to time_stamp
                    if now.hour>=12 and stamp1<=time<stamp2:
                        item['time_stamp'] = time
                        yield Request(url=response.urljoin(href),meta={'item': item, 'pagetype':pagetype},callback=self.parse_namedetail)
                    elif now.hour<12 and stamp3<=time<stamp1:
                        item['time_stamp'] = time
                        yield Request(url=response.urljoin(href), meta={'item': item, 'pagetype':pagetype}, callback=self.parse_namedetail)
                    elif now.hour<12 and time<stamp3:
                        driver.close()
                        print('close',item['category'],time)
                        return
                    elif now.hour>=12 and time<stamp1:
                        driver.close()
                        print('close',item['category'],time)
                        return
                    else:
                        continue
                elif self.flag==0: # flag==0, crawl fixed number pages
                    if time<stamp1:
                        yield Request(url=response.urljoin(href), meta={'item':item, 'pagetype':pagetype}, callback=self.parse_namedetail)
                    else:
                        continue
            #if self.flag==0:
            #    self.page = self.page-1
            driver.find_element_by_xpath("//div[@class='feed-card-page']/span[@class='pagebox_next']/a").click()
            #break
    
    def parse_namedetail(self, response):
        selector = Selector(response)
        # = selector.xpath("""//div[@class="date-source"]/span[@class="date"]/text()""").extract()
        pagetype = response.meta['pagetype']
        item = response.meta['item']
        item['article'] = ''
        if pagetype=='doc':
            article = selector.xpath("""//div[@class="article"]/p/text()""").extract()
            article = '<sep>'.join(article)
            item['article'] = unicodedata.normalize('NFKC',article)
            time_stamp = selector.xpath("//span[@class='date']/text()").extract()[0]
            year, month, day, hour, minute = map(int,map(str.strip, re.split(r"[年月日:]",time_stamp)))
            item['time_stamp'] = datetime.datetime(year=year,
                                                   month=month,
                                                   day=day,
                                                   hour=hour,
                                                   minute=minute)
            item['pagetype'] = 'doc'
        elif pagetype=='img':
            try:
                article = selector.xpath("//meta[@property='og:description']/text()").extract()[0]
            except:
                print(response.url)
            time_stamp = selector.xpath("//em[@class='swpt-time']/text()").extract()[0]
            year, month, day, hour, minute, second = map(int,map(str.strip,re.split(r"[\.:\s]",time_stamp)))
            item['time_stamp'] = datetime.datetime(year=year,
                                                   month=month,
                                                   day=day,
                                                   hour=hour,
                                                   minute=minute)
            item = response.meta['item']
            item['article'] = unicodedata.normalize('NFKC',article)
            item['pagetype'] = 'img'
        elif pagetype=='video':
            article = selector.xpath("//div[@class='vedioinfo_inner']/p[@class='intro']/em[@task='infor']/p/text()").extract()[0]
            time_stamp = selector.xpath("//div[@class='vd_vedioinfo']/div[@class='vedioinfo_inner']/p[@class='from']/span/em/text()").extract()[0]
            year, month, day, hour, minute, second = map(int, map(str.strip, re.split(r"[-:\s]", time_stamp)))
            item['time_stamp'] = datetime.datetime(year=year,
                                                   month=month,
                                                   day=day,
                                                   hour=hour,
                                                   minute=minute)
            item['article'] = unicodedata.normalize('NFKC',article)
            item['pagetype'] = 'video'
        yield item

        

        

            
        
