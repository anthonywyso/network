from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor

from network.items import PlayerItem, PlayerHSItem, PlayerRAPMItem
from network.items import CoachItem, CoachSeasonLogItem
from network.items import ValueItemLoader
from network.pipeline_utilities import DynamicScrapeUtility, regex_xpath

from itertools import izip
import re


class PlayerSpider(CrawlSpider):
    """
    Retrieves all players in NBA universe
    """
    name = "players_scrape"
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
        players = response.xpath("//tbody/tr")
        for player in players:
            loader = ValueItemLoader(item=PlayerItem(), selector=player)
            loader.add_xpath('name', 'td/descendant::a[contains(@href, "players")]/text()')
            loader.add_xpath('id', 'td/descendant::a[contains(@href, "players")]/@href', re="\w+\d")
            loader.add_xpath('college', 'td/a[contains(@href, "college")]/text()')
            loader.add_xpath('college_id', 'td/descendant::a[contains(@href, "college")]/@href', re="(?<==)\w+")
            loader.add_xpath('pos', 'td[@align="center"]/text()')
            yield loader.load_item()


class PlayerHSSpider(CrawlSpider):
    """
    Retrieves all available high schools of NBA universe
    """
    name = "players_hs_scrape"
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
        players = response.xpath("//tbody/tr")
        for player in players:
            loader = ValueItemLoader(item=PlayerHSItem(), selector=player)
            loader.add_xpath('name', 'td/descendant::a[contains(@href, "players")]/text()')
            loader.add_xpath('id', 'td/descendant::a[contains(@href, "players")]/@href', re="\w+\d")
            loader.add_value('highschool', player.xpath('td[5]/text()').extract())
            loader.add_value('highschool_city', player.xpath('td[4]/text()').extract())
            loader.add_value('highschool_state', response.url, re="(?<==)\w+")
            yield loader.load_item()


class PlayerRAPMSpider(CrawlSpider):
    """
    Retrieves all available player RAPM records
    Does not account for 2014 RAPM due to different table format from source
    """
    name = "players_rapm_scrape"
    allowed_domains = ["appspot.com"]
    start_urls = ["http://stats-for-the-nba.appspot.com/"]
    rules = (
        Rule(
            LxmlLinkExtractor(restrict_xpaths="//table/descendant::a[contains(@href, 'ratings')]"),
            callback='parse_crawl',
            follow=True
            ),
    )
    def parse_crawl(self, response):
        players = response.xpath("//table/descendant::tr")
        for player in players:
            loader = ValueItemLoader(item=PlayerRAPMItem(), selector=player)
            loader.add_value('season', response.url, re="(?<=ratings/)\w+")
            for i, value in izip(range(1, 6), ['name', 'rapm_off', 'rapm_def', 'rapm_both', 'poss']):
                loader.add_xpath(value, 'td[%s]/descendant::text()' % str(i))
            yield loader.load_item()


class PlayerRAPMNewSpider(Spider):
    """
    Retrieves player RAPM for 2014
    Accounts for 2014 RAPM due to different table format from source
    """
    name = "players_rapm_new_scrape"
    allowed_domains = ["appspot.com"]
    start_urls = ["http://stats-for-the-nba.appspot.com/ratings/2014.html"]

    def parse(self, response):
        players = response.xpath("//table/descendant::tr")
        for player in players:
            loader = ValueItemLoader(item=PlayerRAPMItem(), selector=player)
            loader.add_value('season', response.url, re="(?<=ratings/)\w+")
            for i, value in izip([2, 3, 4, 5, 8], ['name', 'rapm_off', 'rapm_def', 'rapm_both', 'poss']):
                loader.add_xpath(value, 'td[%s]/descendant::text()' % str(i))
            yield loader.load_item()


class CoachSpider(Spider):
    """
    Retrieves all coaches in NBA universe
    """
    name = "coaches_scrape"
    allowed_domains = ["basketball-reference.com"]
    start_urls = ["http://www.basketball-reference.com/coaches/"]

    def parse(self, response):
        coaches = response.xpath("//tbody/tr")
        for coach in coaches:
            loader = ValueItemLoader(item=CoachItem(), selector=coach)
            loader.add_xpath('name', 'td/descendant::a[contains(@href, "coach")]/text()')
            loader.add_xpath('id', 'td/descendant::a[contains(@href, "coach")]/@href', re="\w+\d")
            loader.add_xpath('college', 'td/a[contains(@href, "college")]/text()')
            yield loader.load_item()


class CoachSeasonLogSpider(CrawlSpider):
    """
    Retrieves season-aggregated coach records
    """
    name = "coaches_seasonlog_scrape"
    allowed_domains = ["basketball-reference.com"]
    start_urls = ["http://www.basketball-reference.com/coaches/"]
    rules = (
        Rule(
            LxmlLinkExtractor(restrict_xpaths="//table[@id='coaches']/descendant::a[contains(@href, 'coach')]"),
            callback='parse_crawl',
            follow=True
            ),
    )

    def parse_crawl(self, response):
        seasons = response.xpath("//table[@id='stats']/descendant::tbody/tr")
        for season in seasons:
            loader = ValueItemLoader(item=CoachSeasonLogItem(), selector=season)
            loader.add_value('id', response.url, re="\w+\d")
            for i, value in izip([1, 2, 3, 4, 5, 6, 7, 10], ['season', 'age', 'league', 'team', 'gp', 'w', 'l', 'standing']):
                loader.add_xpath(value, 'td[%s]/descendant::text()' % str(i))
            yield loader.load_item()


# TODO implement this
class CoachSeasonLogSpider(CrawlSpider):
    """
    Retrieves all coaches in college universe
    """
    name = "coaches_college_scrape"
    allowed_domains = ["sports-reference.com"]
    start_urls = ["http://www.sports-reference.com/cbb/coaches/"]
    rules = (
        Rule(
            LxmlLinkExtractor(restrict_xpaths="//table/descendant::td[contains(@class, 'xx_large_text')]/a"),
            callback='parse_crawl',
            follow=True
            ),
    )

    def parse_crawl(self, response):
        pass

# TODO remove redundancy for basic/adv scraping
class PlayerGameLogSpider(CrawlSpider):
    """
    Retrieves all game-aggregated player records
    """
    name = "players_gamelog_scrape"
    allowed_domains = ["basketball-reference.com"]
    start_urls = ["http://www.basketball-reference.com/players/"]
    rules = (
        Rule(LxmlLinkExtractor(restrict_xpaths="//table/descendant::td[contains(@class, 'xx_large_text')]/a"), follow=True),
        Rule(LxmlLinkExtractor(restrict_xpaths="//table[@id='players']/descendant::td/a[contains(@href, 'players')]"), follow=True),
        Rule(LxmlLinkExtractor(restrict_xpaths="//*[.='Game Logs']/parent::*/descendant::a[contains(@href, 'gamelog')]"), follow=True, callback='parse_crawl'),
    )

    def parse_crawl(self, response):
        extra_features = ["game_type", "player_id", "season"]

        basics = response.xpath("//div[contains(@id, 'div_pgl_basic')]/descendant::tr[@id]")
        basic_header = response.xpath("//div[contains(@id, 'basic_div')]/descendant::thead/descendant::th/@data-stat").extract()
        basic_dynamic = DynamicScrapeUtility("players_gamelog_basic")
        basic_dynamic.extract_table_features(basic_header)
        basic_dynamic.append_table_features(add_features=extra_features)
        basic_dynamic.create_item_class()
        basic_dynamic.create_table()

        advs = response.xpath("//div[contains(@id, 'div_pgl_advanced')]/descendant::tr[@id]")
        adv_header = response.xpath("//div[contains(@id, 'advanced_div')]/descendant::thead/descendant::th/@data-stat").extract()
        adv_dynamic = DynamicScrapeUtility("players_gamelog_adv")
        adv_dynamic.extract_table_features(adv_header)
        adv_dynamic.append_table_features(add_features=extra_features)
        adv_dynamic.create_item_class()
        adv_dynamic.create_table()

        for row in basics:
            loader = ValueItemLoader(item=basic_dynamic.item(), selector=row)
            for i, feature in enumerate(basic_dynamic.features_scraped):
                loader.add_xpath(feature, 'td[%s]/descendant::text()' % str(i+1))
            if regex_xpath("playoffs", row.xpath("@id").extract()):
                loader.add_value("game_type", "post")
            else:
                loader.add_value("game_type", "regular")
            loader.add_value("player_id", re.findall("\w+\d", response.url)[0])
            loader.add_value("season", re.findall("\d{4}", response.url)[0])
            yield loader.load_item()

        for row_adv in advs:
            loader_adv = ValueItemLoader(item=adv_dynamic.item(), selector=row_adv)
            for i_adv, feature_adv in enumerate(adv_dynamic.features_scraped):
                loader_adv.add_xpath(feature_adv, 'td[%s]/descendant::text()' % str(i_adv+1))
            if regex_xpath("playoffs", row_adv.xpath("@id").extract()):
                loader_adv.add_value("game_type", "post")
            else:
                loader_adv.add_value("game_type", "regular")
            loader_adv.add_value("player_id", re.findall("\w+\d", response.url)[0])
            loader_adv.add_value("season", re.findall("\d{4}", response.url)[0])
            yield loader_adv.load_item()
