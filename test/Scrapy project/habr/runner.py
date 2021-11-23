from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from habr import settings
from habr.spiders.habr_ru import HabrRuSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HabrRuSpider)
    process.start()