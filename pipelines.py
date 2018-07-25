# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import pymysql
from bus8684 import settings


class Bus8684Pipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host = settings.MYSQL_HOST,
            db = settings.MYSQL_DBNAME,
            user = settings.MYSQL_USER,
            password = settings.MYSQL_PASSWORD,
            charset = 'utf8',
            use_unicode = True
        )
        self.cursor = self.connect.cursor()
        print("数据库链接成功!!!")

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                "select *  from bus8684 where line_name = %s" , item['line_name']
            )

            repetition = self.cursor.fetchone()
            print(repetition)
            if repetition:
                print(item['line_name'] +"重复")
            else:
                stations = ''
                stations_list = item['bus_stations']
                for station in stations_list:
                    stations += ' ' + station
                self.cursor.execute(
                    'insert into bus8684(`province`, `city`,`line_name`,`line_attribute`,`ticket_price`,`run_time`, `company`,`update_time`, `bus_stations`) values (%s,%s,%s, %s,%s,%s,%s, %s,%s)',
                    (
                        # item['bus_line_url'],
                        # item['lines_url'],
                        item['province'],
                        item['city'],
                        # item['city_url'],
                        item['line_name'],
                        item['line_attribute'],
                        item['ticket_price'],
                        item['run_time'],
                        item['company'],
                        item['update_time'],
                        stations.strip(),
                    )
                )

                self.connect.commit()
        except Exception as error:
            print(
                item['province'],
                item['city'],
                # item['city_url'],
                item['line_name'],
                item['line_attribute'],
                item['ticket_price'],
                item['run_time'],
                item['company'],
                item['update_time'],
                str(item['bus_stations']),
            )
            print("插入出错" + str(error))
        return item

class JsonPipelines(object):
    def __init__(self):
        self.file = open('crawls/bus8684.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()