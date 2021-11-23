import scrapy
from scrapy.http import HtmlResponse
from ..items import HabrParserItem
from scrapy.loader import ItemLoader


class HabrRuSpider(scrapy.Spider):
    name = 'habr_ru'
    allowed_domains = ['habr.com']
    start_urls = ['http://habr.com/']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://habr.com/ru/all/']

    def parse(self, response: HtmlResponse):

        next_page = response.xpath('//a[@id="pagination-next-page"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        article_links = response.xpath('//a[@class = "tm-article-snippet__title-link"]/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_item)

    def parse_item(self, response):
        item_loaded = ItemLoader(item=HabrParserItem(), response=response)
        # item_loaded.add_xpath('author', '//span[@class = "tm-user-info tm-article-snippet__author"]/a/@title'),
        item_loaded.add_value('urls', response.url)
        item_loaded.add_xpath('name',
                              '//h1[@class = "tm-article-snippet__title tm-article-snippet__title_h1"]/span/text()')
        item_loaded.add_xpath('image', '//div[@id = "post-content-body"]/div/figure/*/@data-src')
        # item_loaded.add_xpath('text', '//div[@id="post-content-body"]/div/text()|'
        #                               '//div[@id="post-content-body"]/div/*/text()')
        item_loaded.add_xpath('text', '//div[@id="post-content-body"]/div/*')

        item_loaded.add_xpath('tag',
                              '//div[@class="tm-article-presenter__meta"]/div[position()=1]/ul/li/a/text()')
        # item_loaded.add_xpath('hub',
                              # '//div[@class="tm-article-presenter__meta"]/div[position()=2]/ul/li/a/text()')
        item_loaded.add_xpath('add_datetime',
                              '//span[@class="tm-article-snippet__datetime-published"]/time/@title')

        yield item_loaded.load_item()

