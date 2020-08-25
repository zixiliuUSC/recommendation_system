from scrapy import cmdline
cmdline.execute("scrapy crawl sina_spider -a page=30 -a flag=0".split())