# -*- coding: utf-8 -*-
import scrapy
from ..items import WallhavenimagesItem


class WallhavenSpider(scrapy.Spider):
    name = 'wallhaven'
    # allowed_domains = ['alpha.wallhaven.cc']
    # start_urls = ['http://alpha.wallhaven.cc/']
    base_url = "https://alpha.wallhaven.cc/latest?page="

    def start_requests(self):
        for i in range(1, 10):
            url = self.base_url + str(i)
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        hrefs = response.xpath("/html/body/main/div[1]/section/ul/li/figure/a[1]/@href").extract()
        index = response.url.split('=')[-1]
        for href in hrefs:
            yield scrapy.Request(url=href, callback=self.get_url, meta={"index": "page" + index})

    def get_url(self, response):
        item = WallhavenimagesItem()
        hrefs = response.xpath("//*[@id='wallpaper']/@src").extract()
        hrefs = ["https:" + href for href in hrefs]
        name = response.meta['index']
        item['imgname'] = name
        item['imgurl'] = hrefs

        yield item
