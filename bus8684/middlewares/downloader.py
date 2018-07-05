import time
from scrapy.exceptions import IgnoreRequest
from scrapy.http import HtmlResponse, Response
from selenium import webdriver
import selenium.webdriver.support.ui as ui


class CustomDownloader(object):
    def __init__(self):
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000
        cap["phantomjs.page.setting.lodaImages"] =True
        cap["phantomjs.page.setting.disk-cache"] =True
        # cap["phantomjs.page.customHeaders.Cookie"] =
        self.driver = webdriver.PhantomJS()
        wait = ui.WebDriverWait(self.driver, 10)

    def VisitPersonPage(self, url):
        print('正在加载网页......')
        self.driver.get(url)
        time.sleep(1)
        js = "var q=document.documentElement.scrollTOP=10000"
        self.driver.execute_script(js)
        time.sleep(5)
        content = self.driver.page_source.encode('gbk', 'ignore')
        print('网页加载完毕......')
        return content

    def __del__(self):
        self.driver.quit()

