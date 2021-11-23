import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join


def process_hub(value):
    return value.replace('\n    ', '').replace('\n  ', '')


def process_datetime(value):

    return value.replace(', ', 'T') + ':09Z'
#   "add_datetime": ""2021-11-21T13:33:09Z"",
#                   '2021-11-21, 13:33'

class HabrParserItem(scrapy.Item):
    _id = scrapy.Field()
    author = scrapy.Field(output_processor=TakeFirst())
    urls = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    # text = scrapy.Field(output_processor=Join(), input_processor=MapCompose(process_text))
    text = scrapy.Field(output_processor=Join())
    image = scrapy.Field()
    tag = scrapy.Field()
    hub = scrapy.Field(input_processor=MapCompose(process_hub))
    add_datetime = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(process_datetime))
