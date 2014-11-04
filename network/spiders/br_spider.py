from scrapy.spider import Spider
from scrapy.selector import Selector

# TODO implement this spider with crawl
class BRSpider(Spider):

    def parse(self, response):
        sel = Selector(response)
        yield