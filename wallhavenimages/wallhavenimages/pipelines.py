# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import re


class WallhavenimagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['imgurl']:
            yield Request(image_url, meta={'name': item['imgname']})

    # def process_item(self, item, spider):
    #     return item

    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        name = request.meta['name']
        name = re.sub(r'[？\\*|“<>:/]', '', name)
        filename = u'{0}/{1}'.format(name, image_guid)
        print(filename)
        return filename
