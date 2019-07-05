# -*- coding: utf-8 -*-
import scrapy
from ..items import BiqugedownloadItem


class BiqugespiderSpider(scrapy.Spider):
    name = 'biqugespider'
    allowed_domains = ['www.xbiquge.la']
    start_urls = ['http://www.xbiquge.la/xiaoshuodaquan/']
    BASE_URL = "http://www.xbiquge.la"

    def parse(self, response):
        """
        获取小说的网址
        :param response:
        :return:
        """
        lis = response.css("html body div#wrapper div#main div.novellist ul li")
        for li in lis:
            href = li.xpath('a/@href').get()
            yield scrapy.Request(href, callback=self.get_chapters)

    def get_chapters(self, response):
        """
        获取小说章节的网址等信息
        :param response:
        :return:
        """
        titlename = response.css("html body div#wrapper div.box_con div#maininfo div#info h1::text").get()
        p = response.css("html body div#wrapper div.box_con div#maininfo div#info p::text").getall()

        author = p[0].split("：")[-1]
        last_update_time = p[-2]
        introducation = response.css("html body div#wrapper div.box_con div#maininfo div#intro p::text").getall()
        introducation = "".join([text.replace("\r\n", "").strip() for text in introducation])
        dds = response.css("html body div#wrapper div.box_con div#list dl dd")
        for dd in dds:
            href = dd.xpath('a/@href').get()
            chaptername = dd.xpath('a/text()').get()
            url = self.BASE_URL + href
            yield scrapy.Request(url, callback=self.get_content,
                                 meta={"titlename": titlename, "author": author, "last_update_time": last_update_time,
                                       "introducation": introducation,
                                       "chaptername": chaptername})

    def get_content(self, response):
        content = response.css("html body div#wrapper div.content_read div.box_con div#content::text").getall()
        id = response.url.split('/')[-1].split('.')[0]
        titlename = response.meta['titlename']
        chaptername = response.meta['chaptername']
        last_update_time = response.meta['last_update_time']
        introducation = response.meta['introducation']
        author = response.meta['author']

        item = BiqugedownloadItem()
        item['content'] = content
        item['id'] = id
        item['titlename'] = titlename
        item['chaptername'] = chaptername
        item['last_update_time'] = last_update_time
        item['introducation'] = introducation
        item['author'] = author
        yield item
