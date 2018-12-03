# -*- coding: utf-8 -*-
import scrapy


class DailirenSpider(scrapy.Spider):
    name = 'dailiren'
    allowed_domains = ['winbaoxian.cn']
    start_urls = ['http://winbaoxian.cn/']

    def parse(self, response):
        pass
