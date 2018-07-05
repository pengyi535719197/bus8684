import scrapy
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from bus8684.items import Bus8684Item



class BusSpider(scrapy.Spider):
    name = 'bus8684'
    allowed_domains = ['8684.cn']
    start_urls = ['http://www.8684.cn/']

    def parse(self, response):
        pass


    def get_url(self,response):

        # browser = webdriver.Firefox(executable_path="D:\\firefox\\geckodriver.exe")
        # browser = webdriver.PhantomJS()

        options = Options()
        options.add_argument("-headless")
        browser = Firefox(executable_path="D:\\firefox\\geckodriver.exe", firefox_options=options)


        browser.get("http://www.8684.cn/")
        elem = browser.find_element_by_css_selector(".addrChangeBus")
        elem.click()

        soup = BeautifulSoup(browser.page_source, 'lxml')
        provinces = soup.select("#city0 > li")
        # cities = soup.select("#city0 > li > i > a")
        browser.quit()
        city_url = dict()

        for province in provinces:
            cities = province.select("> i > a")
            for city in cities:
                item = Bus8684Item()
                # print(city.string.extract())
                item["province"] = province.select("> cite")[0].get_text()
                item["city"] = city.get_text()
                item["city_url"] = city.get("href")
                # city_url[city.get_text()] = city.get("href")
                yield scrapy.Request(item["city_url"], callback=self.parse())

