# -*- coding: utf-8 -*-
import scrapy
from bus8684.items import Dt8684Item

class Dt8684Spider(scrapy.Spider):
    name = "dt8684"
    allowed_domains = ["8684.cn"]
    start_urls = ['http://dt.8684.cn/']

    def parse(self, response):
        cities = response.xpath('//div[@class="li_right line"]/a')
        item_1 = []
        for City in cities:
            item = Dt8684Item()
            item['city'] = City.xpath('.//text()').extract_first()[:-2]
            city_url = City.xpath('.//@href').extract_first()
            item['city_url'] = city_url
            item_1.append(item)
        for item in item_1:
            yield scrapy.Request(item['city_url'], callback=self.city_parse, meta={'item_1': item})

    def city_parse(self, response):
        item_1 = response.meta['item_1']
        item_2 = []
        dt_lines = response.xpath('//a[@class="cm-tt"]')
        for dt_line in dt_lines:
            item = Dt8684Item()
            item['city'] = item_1['city']
            item['city_url'] = item_1['city_url']
            item['line_name'] = dt_line.xpath('.//text()').extract_first()
            line_url = dt_line.xpath('.//@href').extract_first()
            item['line_url'] = item_1['city_url'] + line_url
            item_2.append(item)
        for item in item_2:
            yield scrapy.Request(url=item['line_url'], callback=self.line_parse, meta={'item_2': item})

    def line_parse(self, response):
        item_2 = response.meta['item_2']
        stations = response.xpath('//table[@class="pi-table tl-table"]//tbody')
        item = Dt8684Item()
        item['city'] = item_2['city']
        item['city_url'] = item_2['city_url']
        item['line_name'] = item_2['line_name']
        item['line_url'] = item_2['line_url']
        item['stations'] = stations.xpath('.//tr/td/a/text()').extract()
        item['start_time1'] = stations.xpath('.//tr/td[2]/text()').extract()
        item['start_time2'] = stations.xpath('.//tr/td[3]/text()').extract()
        item['end_time1'] = stations.xpath('.//tr/td[4]/text()').extract()
        item['end_time2'] = stations.xpath('.//tr/td[5]/text()').extract()
        yield item
