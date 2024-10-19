BOT_NAME = 'hepsiemlak_scraper'

SPIDER_MODULES = ['hepsiemlak_scraper.spiders']
NEWSPIDER_MODULE = 'hepsiemlak_scraper.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Download delay (set a delay of 2 seconds between requests)
DOWNLOAD_DELAY = 2

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 1

# Enable retries
RETRY_ENABLED = True
RETRY_TIMES = 5  # Retry many times since proxies often fail

# Enable a user-agent rotation
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
}

# Set feed export encoding
FEED_EXPORT_ENCODING = 'utf-8'
