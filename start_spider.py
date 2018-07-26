from scrapy import cmdline

def start_bus8684(city = '厦门'):
    cmdline.execute(('scrapy crawl bus8684 -a crawl_city=[%s]' % city).split())


if __name__ == '__main__':
    start_bus8684(['上海'])