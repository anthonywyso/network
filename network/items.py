# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class NetworkItem(Item):
    # define the fields for your item here like:
    name = Field()
    name_hs = Field()
    loc_hs = Field()
    name_college = Field()
    trans_type = Field()
    trans_team = Field()

    pass