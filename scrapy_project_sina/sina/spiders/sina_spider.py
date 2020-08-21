# -*- coding: utf-8 -*-
import scrapy
import selenium
from selenium import webdriver
from scrapy.http import Request
from items import *
from scrapy import Selector
import os
import pandas as pd
import unicodedata

class SinaSpiderSpider(scrapy.Spider):
    name = 'sina_spider'
    allowed_domains = ['sina.com.cn']
    
    def __init__(self, *args, **kwargs):
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

        self.directory = "M:\\scrapy_project\\recommendation_system\\scrapy_project_sina\\data"
        self.page = 1 # 目前是不合理的，要从外面传进来
        self.flag = -1 # 暂时定义这个变量，后面会用到


    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)
            #break


    def parse(self, response):
        #self.logger.info(response.text)
        driver = webdriver.Chrome(chrome_options=self.options)
        driver.set_page_load_timeout(100)
        driver.get(response.url)
        for i in range(self.page):
        #for i in range(self.page):
            while not driver.find_element_by_xpath("//div[@class='feed-card-page']").text:
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);") # selenium的driver类可以用execute_script()函数在浏览器内部执行JavaScript。
            count = driver.find_elements_by_xpath("//h2[@class='undefined']/a[@target='_blank']")
            for each in count:
                title = each.text
                if response.url == "https://ent.sina.com.cn/zongyi/":
                    item = zongyiItem()
                    item['category'] = 'zongyi'
                elif response.url == "https://news.sina.com.cn/china/":
                    item = ChinaItem()
                    item['category'] = 'China'
                else:
                    item = filmItem()
                    item['category'] = 'film'
                #item.article = ''
                item['title'] = unicodedata.normalize('NFKC',title)
                href = each.get_attribute('href')
                yield Request(url=response.urljoin(href), meta={'item':item}, callback=self.parse_namedetail)
            driver.find_element_by_xpath("//div[@class='feed-card-page']/span[@class='pagebox_next']/a").click()
            #break
    
    def parse_namedetail(self, response):
        selector = Selector(response)
        time = selector.xpath("""//div[@class="date-source"]/span[@class="date"]/text()""").extract()
        article = selector.xpath("""//div[@class="article"]/p/text()""").extract()
        item = response.meta['item']
        article = '<sep>'.join(article)
        item['time_stamp'] = unicodedata.normalize('NFKC',time[0])
        item['article'] = unicodedata.normalize('NFKC',article)
        #print(item['title'])
        #print(item['time_stamp'])
        #print(item['article'])
        
        #path = os.path.join(self.directory,item['category']+'.csv')
        
        #data = {'title':[item['title']],'time_stamp':[item['time_stamp']], 'article':[item['article']]}
        #if not os.path.exists(path):
        #    pd.DataFrame(data).to_csv(path, mode='w')
        #else:
        #    pd.DataFrame(data).to_csv(path, mode='a', header=False)
        
        yield item
        

            
        
