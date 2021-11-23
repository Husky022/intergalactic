
BOT_NAME = 'habr'

SPIDER_MODULES = ['habr.spiders']
NEWSPIDER_MODULE = 'habr.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'

ROBOTSTXT_OBEY = False

LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'

ITEM_PIPELINES = {
   'habr.pipelines.HabrPipeline': 200,
   'habr.pipelines.HabrPipelineJson': 300,
}

IMAGES_STORE = 'photos'

DOWNLOAD_DELAY = 1