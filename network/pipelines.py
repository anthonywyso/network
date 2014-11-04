# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import py2neo

#TODO implement this pipeline
class Neo4jPipeline(object):
    name = "br"
    allowed_domains = ["basketball-reference.com"]
    start_urls = [
        "http://www.basketball-reference.com/leagues/NBA_2014_totals.html",
        "http://www.basketball-reference.com/coaches/"
    ]


    def process_item(self, item, spider):
        '''
        Converts custom Scrapy Item and processes it into Neo4j database
        INPUT:
        OUTPUT:
        '''
        return item
