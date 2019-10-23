# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class TencentPipeline(object):
    def open_spider(self, spider):
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='83117973bb',
                                  database='tencentdb',
                                  charset='utf8',
                                  port=3306)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()

    def process_item(self, item, spider):
        try:
            ins = 'insert into tencenttab values(%s,%s,%s,%s,%s,%s);'
            L = [
                item['job_name'],
                item['job_type'],
                item['job_duty'],
                item['job_require'],
                item['job_address'],
                item['job_time']
            ]
            # print(L)
            self.cursor.execute(ins, L)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print("EEROR", e)

        return item
