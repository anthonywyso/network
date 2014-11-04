# Scrapy settings for network project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'network'

SPIDER_MODULES = ['network.spiders']
NEWSPIDER_MODULE = 'network.spiders'

DOWNLOAD_DELAY = 120.0
RANDOMIZE_DOWNLOAD_DELAY = True
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1

COOKIES_ENABLED = False

ITEM_PIPELINES = {
    'cba.pipelines.SQLitePipeline': 300
}

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0 # Set to 0 to never expire

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'network (+http://www.yourdomain.com)'
