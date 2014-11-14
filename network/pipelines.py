# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
import sqlite3 as sql
import pandas as pd
import numpy as np

import settings


# resolve this pipeline -- currently processes each line item individually with its own header row (due to way spider yields data)
# deprecated, all spiders now run through SQLExportPipeLine into their own "scrape"
class CsvExportPipeline(object):

    def process_item(self, item, spider):
        exporter = CsvItemExporter(open('data/%s.csv' % spider.name, 'a+b'), include_headers_line=False)
        exporter.export_item(item)
        return item


class SQLExportPipeline(object):

    def __init__(self):
        """
        Declares sqlite database.
        """
        self.db = settings.DATABASE['database']

    def process_item(self, item, spider):
        """
        Processes scrapy item and inserts it into existing db table.
        This method is called for every item pipeline component.
        """
        features = item.keys()
        data = {feature: item[feature] for feature in features}
        df = pd.DataFrame(data=data, index=np.arange(1))

        with sql.connect(self.db) as connection:
            # df.to_sql(spider.name, connection, if_exists='append')
            df.to_sql(item.__class__.__name__, connection, if_exists='append')
        return item