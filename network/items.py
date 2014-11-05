# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst


class PlayerItem(Item):
    name = Field()
    id = Field()
    college = Field()
    pos = Field()


class PlayerHSItem(Item):
    name = Field()
    id = Field()
    highschool = Field()
    highschool_city = Field()
    highschool_state = Field()


class CoachItem(Item):
    name = Field()
    id = Field()
    college = Field()


class CoachSeasonLogItem(Item):
    id = Field()
    season = Field()
    age = Field()
    league = Field()
    team = Field()
    gp = Field()
    w = Field()
    l = Field()
    standing = Field()


class ValueItemLoader(ItemLoader):
    default_output_processor = TakeFirst()