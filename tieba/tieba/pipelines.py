# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
class TiebaPipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for url in item['url']:
            yield Request(
                url,
                meta={'item':item}
            )
    def file_path(self, request, response=None, info=None):
        url=request.url
        file_name=url.split('/')[-1]
        title=request.meta['item']['title']
        path=title+'/'+file_name
        return path
    def item_completed(self, results, item, info):
        image_path=[x['path'] for ok,x in results if ok]
        if not image_path:
            raise DropItem("Contain No Images")
        return item







class MyMongDBPipeline(object):
    MONGO_URL='mongodb://localhost:27017'
    MONGO_DB='tieba'

    def open_spider(self,spider):
        self.client=pymongo.MongoClient(self.MONGO_URL)
        self.db=self.client[self.MONGO_DB]
    def process_item(self,item,spider):
        collection=self.db[spider.name]
        collection.insert(dict(item))
        return item
    def close_spider(self,spider):
        self.client.close()



