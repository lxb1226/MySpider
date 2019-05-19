# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os


class NoveldownloadPipeline(object):
    def process_item(self, item, spider):
        curPath = 'F:\\笔趣阁小说'
        tempPath = str(item['titlename'])
        targetPath = curPath + os.path.sep + tempPath
        if not os.path.exists(targetPath):
            os.makedirs(targetPath)
        filename_path = 'F:\\笔趣阁小说' + os.path.sep + str(item['titlename']) + os.path.sep + str(
            item['chaptername']) + '.txt'
        with open(filename_path, 'w', encoding='utf-8') as f:
            f.write(item['text'] + "\n")

        return item
