# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem


class ThirtysixkrPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(settings['MONGODB_HOST'], settings['MONGODB_PORT'])
        db = client[settings['MONGODB_DB']]
        self.post = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.post.insert(dict(item))
        return item

