# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Bus8684Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    province = scrapy.Field()
    city = scrapy.Field()
    city_url = scrapy.Field()
    lines_url = scrapy.Field()
    bus_line_url = scrapy.Field()
    bus_stations = scrapy.Field()
    line_name = scrapy.Field()
    line_attribute = scrapy.Field()
    ticket_price = scrapy.Field()
    run_time = scrapy.Field()
    company = scrapy.Field()
    update_time = scrapy.Field()

class Dt8684Item(scrapy.Item):
    city = scrapy.Field()
    city_url = scrapy.Field()
    line_name = scrapy.Field()
    line_url = scrapy.Field()
    stations = scrapy.Field()
    start_time1 = scrapy.Field()
    start_time2 = scrapy.Field()
    end_time1 = scrapy.Field()
    end_time2 = scrapy.Field()