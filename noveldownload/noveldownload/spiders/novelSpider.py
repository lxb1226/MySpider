# -*- coding: utf-8 -*-
import scrapy

from ..items import NoveldownloadItem


class NovelspiderSpider(scrapy.Spider):
    name = 'novelSpider'
    allowed_domains = ['www.biquge5.com']
    start_urls = [
        'https://www.biquge5.com/shuku/1/allvisit-0-1.html',
        'https://www.biquge5.com/shuku/2/allvisit-0-1.html',
        'https://www.biquge5.com/shuku/3/allvisit-0-1.html',
        'https://www.biquge5.com/shuku/5/allvisit-0-1.html',
        'https://www.biquge5.com/shuku/6/allvisit-0-1.html']

    def parse(self, response):
        lis = response.xpath("/html/body/div[2]/div[1]/ul[@class='list-group list-top']/li")
        for li in lis:
            href = li.xpath("./div[1]/div[1]/a/@href").get()
            yield scrapy.Request(url=href, callback=self.parse_novel_html)

    def parse_novel_html(self, response):
        lis = response.xpath(
            '/html/body/div[@id="wrapper"]/div[@class="box_con"]/div[@id="list"]/ul[@class="_chapter"]/li')
        for li in lis:
            href = li.xpath('./a/@href').get()
            name = li.xpath('./a/text()').get()
            yield scrapy.Request(url=href, callback=self.download_text, meta={"name": name})

    def download_text(self, response):
        text = response.xpath('//*[@id="content"]/text()').get()
        titlename = response.xpath(
            "//div[@id='wrapper']/div[@class='content_read']/div[@class='box_con']/div[@class='con_top']/a[3]/text()").get()

        item = NoveldownloadItem()
        item['chaptername'] = response.meta['name']
        item['text'] = text
        item['titlename'] = titlename

        yield item
