from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader

from network.items import PlayerItem, PlayerHSItem, CoachItem, CoachSeasonLogItem
from network.items import ValueItemLoader

from itertools import izip
import re


# TODO go into player/coach profiles to identify pro team status
class PlayerSpider(CrawlSpider):
    '''
    USAGE: scrapy crawl players --set FEED_URI=data/players.csv --set FEED_FORMAT=csv
    '''
    name = "players"
    allowed_domains = ["basketball-reference.com"]
    start_urls = ["http://www.basketball-reference.com/players/"]
    rules = (
        Rule(
            LxmlLinkExtractor(restrict_xpaths="//table/descendant::td[contains(@class, 'xx_large_text')]/a"),
            callback='parse_start_url',
            follow=True
            ),
    )

    def parse_start_url(self, response):
        sel = Selector(response)
        players = sel.xpath("//tbody/tr")
        for player in players:
            loader = ItemLoader(item=PlayerItem(), selector=player)
            loader.add_xpath('name', 'td/descendant::a[contains(@href, "players")]/text()')
            loader.add_xpath('id', 'td/descendant::a[contains(@href, "players")]/@href', re="\w+\d")
            loader.add_xpath('college', 'td/a[contains(@href, "college")]/text()')
            loader.add_xpath('pos', 'td[@align="center"]/text()')
            yield loader.load_item()


class PlayerHSSpider(CrawlSpider):
    '''
    USAGE: scrapy crawl players_hs --set FEED_URI=data/players_hs.csv --set FEED_FORMAT=csv
    '''
    name = "players_hs"
    allowed_domains = ["basketball-reference.com"]
    start_urls = ["http://www.basketball-reference.com/friv/high_schools.cgi"]
    rules = (
        Rule(
            LxmlLinkExtractor(restrict_xpaths="//a[contains(@href, 'high_schools')]"),
            callback='parse_start_url',
            follow=True
            ),
    )

    def parse_start_url(self, response):
        sel = Selector(response)
        players = sel.xpath("//tbody/tr")
        for player in players:
            loader = ValueItemLoader(item=PlayerHSItem(), selector=player)
            loader.add_xpath('name', 'td/descendant::a[contains(@href, "players")]/text()')
            loader.add_xpath('id', 'td/descendant::a[contains(@href, "players")]/@href', re="\w+\d")
            loader.add_value('highschool', player.xpath('td[5]/text()').extract())
            loader.add_value('highschool_city', player.xpath('td[4]/text()').extract())
            loader.add_value('highschool_state', response.url, re="(?<==)\w+")
            yield loader.load_item()


class CoachSpider(Spider):
    '''
    USAGE: scrapy crawl coaches --set FEED_URI=data/coaches.csv --set FEED_FORMAT=csv
    '''
    name = "coaches"
    allowed_domains = ["basketball-reference.com"]
    start_urls = [
        "http://www.basketball-reference.com/coaches/"
    ]

    def parse(self, response):
        sel = Selector(response)
        coaches = sel.xpath("//tbody/tr")
        for coach in coaches:
            loader = ItemLoader(item=CoachItem(), selector=coach)
            loader.add_xpath('name', 'td/descendant::a[contains(@href, "coach")]/text()')
            loader.add_xpath('id', 'td/descendant::a[contains(@href, "coach")]/@href', re="\w+\d")
            loader.add_xpath('college', 'td/a[contains(@href, "college")]/text()')
            yield loader.load_item()


class CoachSeasonLogSpider(CrawlSpider):
    '''
    USAGE: scrapy crawl coaches_seasonlog --set FEED_URI=data/coaches_seasonlog.csv --set FEED_FORMAT=csv
    '''
    name = "coaches_seasonlog"
    allowed_domains = ["basketball-reference.com"]
    start_urls = [
        "http://www.basketball-reference.com/coaches/"
    ]
    rules = (
        Rule(
            LxmlLinkExtractor(restrict_xpaths="//table[@id='coaches']/descendant::a[contains(@href, 'coach')]"),
            callback='parse_history',
            follow=True
            ),
    )

    def parse_history(self, response):
        sel = Selector(response)
        seasons = sel.xpath("//table[@id='stats']/descendant::tbody/tr")
        for season in seasons:
            loader = ValueItemLoader(item=CoachSeasonLogItem(), selector=season)
            loader.add_value('id', response.url, re="\w+\d")
            # re.findall('\d{2}', season.xpath("td[%s]/descendant::text()"))  # TODO change season to a single value
            # loader.add_value('season', season.xpath("td[%s]/descendant::text()"), re="\w+\d")
            for i, value in izip([1, 2, 3, 4, 5, 6, 7, 10], ['season', 'age', 'league', 'team', 'gp', 'w', 'l', 'standing']):
                loader.add_xpath(value, 'td[%s]/descendant::text()' % str(i))
            yield loader.load_item()
