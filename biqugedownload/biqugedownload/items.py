# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BiqugedownloadItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    titlename = scrapy.Field()
    chaptername = scrapy.Field()
    last_update_time = scrapy.Field()
    id = scrapy.Field()
    introducation = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
