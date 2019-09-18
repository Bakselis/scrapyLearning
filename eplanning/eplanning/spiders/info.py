# -*- coding: utf-8 -*-
import scrapy


class InfoSpider(scrapy.Spider):
    name = 'info'
    allowed_domains = ['http://www.eplanning.ie/']
    start_urls = ['http://http://www.eplanning.ie//']

    def parse(self, response):
        pass
