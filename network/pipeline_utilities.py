from scrapy.item import Item, Field

import settings

import re
import sqlite3 as sql


def clean_values(feature):
    """
    INPUT: string
    OUTPUT: string
    Formats feature values so they can be used in sqlite schema
    """
    # TODO exceptions.UnicodeEncodeError: 'ascii' codec can't encode character u'\xa0' in position 0: ordinal not in range(128)
    feature = feature.strip().lower()
    feature = feature.replace('%', 'pct')
    feature = feature.replace('3p', 'fg3')
    feature = feature.replace(' ', '_')
    feature = feature.replace('/', '_')
    feature = feature.replace('&', 'and')
    feature = feature.replace("'s", '')
    feature = feature.replace("#", "num")
    if re.match('\d', feature):
        feature = "_" + feature
    return feature


def regex_xpath(search, xpath):
    return re.findall(str(search), xpath.extract()[0])


class DynamicScrapeUtility(object):

    def __init__(self, dbtable, features=[]):
        self.features = list(features)
        self.features_scraped = list(features)
        self.table = dbtable
        self.item = None

    def extract_table_features(self, header):
        """
        INPUT: list
        OUTPUT: None
        Builds list of features from a table's header
        """
        for col in header:
            f = clean_values(col)
            self.features.append(f)
            self.features_scraped.append(f)

    def append_table_features(self, add_features):
        """
        INPUT: list
        OUTPUT: None
        Adds specified to list of features
        """
        for f in add_features:
            feature = clean_values(f)
            self.features.append(feature)

    def create_item_class(self):
        """
        INPUT: str, list
        OUTPUT: Item
        Creates a dynamic scrapy item object
        """
        fields_dict = {}
        for field in self.features:
            fields_dict[field] = Field()
        self.item = type(self.table, (Item,), fields_dict)

    def create_table(self):
        """
        INPUT: string
        OUTPUT: None
        Create db table with schema. db attributes specified in settings
        """
        sql_query = "CREATE TABLE IF NOT EXISTS {0} (sys_id INTEGER PRIMARY KEY ASC, {1})".format(self.table, ", ".join(self.features))
        with sql.connect(settings.DATABASE['database']) as connection:
            c = connection.cursor()
            c.execute(sql_query)