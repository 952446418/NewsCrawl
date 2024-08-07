# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from redis import Redis


class Movie1Pipeline:
    conn = None

    def open_spider(self, spider):
        self.conn = spider.conn

    def process_item(self, item, spider):
        dic = {
            'id': item['id'],
            'title': item['title'],
            'video_url': item['video_url']
        }
        print(dic)
        self.conn.lpush('movieData', dic)  # movieData——列表名
        return item

