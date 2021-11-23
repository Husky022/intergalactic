import time
from itemadapter import ItemAdapter
import json
import random


class HabrPipeline:

    def process_item(self, item, spider):
        return item


class HabrPipelineJson:
    def process_item(self, item, spider):
        item_dict = {}
        item_dict['model'] = "mainapp.article"
        item_dict['pk'] = int(time.time())
        item_dict['fields'] = {
            'hub': random.randint(1, 6),
            'name': item['name'],
            'image': item['image'][0],
            'preview': item['text'][:50].replace('<p>', ''),
            'text': item['text'],
            'is_active': True,
            'author': 1,
            'tag':  item['tag'][0],
            "add_datetime": item['add_datetime'],
            "article_status_new": 4,
        }
        line = json.dumps(ItemAdapter(item_dict).asdict(), ensure_ascii=False, indent=4, default=str) + ",\n"
        # line = json.dumps(item, ensure_ascii=False, indent=4, default=str) + ",\n"
        self.file.write(line)
        return item

    def open_spider(self, spider):
        self.file = open('result.json', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()