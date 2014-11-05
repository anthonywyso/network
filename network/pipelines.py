# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
import py2neo

# TODO resolve this pipeline -- currently processes each line item individually with its own header row
class CsvExportPipeline(object):

    def process_item(self, item, spider):
        exporter = CsvItemExporter(open('data/%s.csv' % spider.name, 'a+b'))
        exporter.export_item(item)
        return item


# TODO implement this pipeline
class Neo4jPipeline(object):

    def process_item(self, item, spider):
        '''
        Converts custom Scrapy Item and processes it into Neo4j database
        INPUT:
        OUTPUT:
        '''
        return item

