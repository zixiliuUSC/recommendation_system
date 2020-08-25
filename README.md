# recommendation_system
This repo includes a full stack pipeline of building a recommendation system, which include data crawling, data cleaning, data pre-process, database building and data storage, collaborative filtering based ranking, deep learning method based ranking etc.  

## 2020.8.25 Update 
- Store Crawled data in sqlDB
- Create two crawling mode: 
  - 1. Updating mode: crawl data from 00:00 to 12:00 today or data from 12:00 to 23:59 yesterday, which depends on when you start your task. If starting before 12:00 it will crawl yesterday data and if starting after 12:00, it will crawl today's data. 
  - 2. Initialized mode: this mode is used for initialize your DB. 
- This repo can crawl Hot Spot and normal page in Sina news pages. 
- Usage: 
  - Updating mode: `scrapy crawl sina_spider -a page=1 -a flag=1 # Note: the page here is not valid, since the spider will continue to go to next page until crawl all links that satisfy the time lag.` 
  - Initialized mode: `scrapy crawl sina_spider -a page=30 -a flag=0`
 
- Bugs need to be fixed: 
  - This version set up the skeleton to crawl video page and picture page, but currently the selector in scrapy cannot parse correctly. 
