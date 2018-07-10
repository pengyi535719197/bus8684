import scrapy
import time
import random
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from bus8684.items import Bus8684Item


class BusSpider(scrapy.Spider):
    name = 'bus8684'
    allowed_domains = ['8684.cn']
    start_urls = ['http://www.8684.cn/']

    def parse(self, response):

        options = Options()
        options.add_argument("-headless")
        browser = Firefox(executable_path="D:\\firefox\\geckodriver.exe", firefox_options=options)

        browser.get("http://www.8684.cn/")
        elem = browser.find_element_by_css_selector(".addrChangeBus")
        elem.click()

        soup = BeautifulSoup(browser.page_source, 'lxml')
        provinces = soup.select("#city0 > li")
        browser.quit()

        item_1 = []
        for province in provinces:
            cities = province.select("> i > a")
            for city in cities:
                item = Bus8684Item()
                item["province"] = province.select("> cite")[0].get_text()
                item["city"] = city.get_text()
                city_url = city.get("href")
                item["city_url"] = city_url
                item_1.append(item)
        for item in item_1:
            yield scrapy.Request(url=item['city_url'], callback=self.line_url_parse, meta={'item_1': item})

    def line_url_parse(self, response):
        item_1 = response.meta['item_1']
        items = []
        lines_url = response.xpath('//div[@class="bus_kt_r1" or @class="bus_kt_r2"]//a/@href').extract()
        for line_url in lines_url:
            item = Bus8684Item()
            item['lines_url'] = line_url
            item['province'] = item_1['province']
            item['city'] = item_1['city']
            item['city_url'] = item_1['city_url']
            items.append(item)
        for item in items:
            time.sleep(random.uniform(1, 2))
            url = item['city_url'] + item['lines_url'].split('/')[1]
            yield scrapy.Request(url=url, callback=self.line_parse, meta={'item_2': item})


    def line_parse(self, response):
        item_2 = response.meta['item_2']
        items = []
        lines_urls = response.xpath('//div[@id="con_site_1"]//a/@href').extract()
        for line_url in lines_urls:
            item = Bus8684Item()
            item['bus_line_url'] = line_url
            item['lines_url'] = item_2['lines_url']
            item['province'] = item_2['province']
            item['city'] = item_2['city']
            item['city_url'] = item_2['city_url']
            items.append(item)
        for item in items:
            url = item['city_url'] + item['bus_line_url'].split('/')[1]
            yield scrapy.Request(url=url , callback=self.bus_stations_parse, meta={'item_3': item})

    def bus_stations_parse(self, response):
        item = response.meta['item_3']
        bus_stations = response.xpath('//div[@class="bus_line_site "]/div[1]//div/a/text()').extract()
        item['bus_stations'] = bus_stations
        item['line__name'] = response.xpath('//div[@class="bus_i_t1"]/h1/text()').extract_first()
        item['line_attribute'] = response.xpath('//div[@class="bus_i_t1"]/a/text()').extract_first()
        run_time = response.xpath('//p[@class="bus_i_t4"]/text()').extract()[0]
        ticket_price = response.xpath('//p[@class="bus_i_t4"]/text()').extract()[1]
        update_time = response.xpath('//p[@class="bus_i_t4"]/text()').extract()[-1]

        if len(run_time.split('：')) == 1:
            item['run_time'] = '暂无信息'
        else:
            item['run_time'] = run_time.split('：')[1]

        if len(ticket_price.split('：')) == 1:
            item['ticket_price'] = '暂无信息'
        else:
            item['ticket_price'] = ticket_price.split('：')[-1]

        item['company'] = response.xpath('//p[@class="bus_i_t4"]/a/text()').extract_first()

        if len(update_time.split('：')) == 1:
            item['update_time'] = '暂无信息'
        else:
            item['update_time'] = update_time.split('：')[-1]
        yield item
