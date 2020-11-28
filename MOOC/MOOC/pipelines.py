# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from scrapy.exceptions import DropItem
from pymysql.err import IntegrityError


class MoocPipeline:
    def process_item(self, item, spider):
        return item


class Mysql_Pipeline(object):
    def __init__(self, mysql_host, mysql_db, mysql_user, mysql_passwd):
        self.connect = pymysql.connect(
            host=mysql_host,
            db=mysql_db,
            user=mysql_user,
            passwd=mysql_passwd,
        )
        self.cursor = self.connect.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_db=crawler.settings.get('MYSQL_DBNAME'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_passwd=crawler.settings.get('MYSQL_PASSWD')
        )

    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        # print(data)
        sql = 'insert into %s (%s) values(%s)' % (item.table, keys, values)
        # print(data)
        # print(sql % tuple(data.values()))
        # sql = "INSERT INTO quotes_spider(author,tags,text) VALUES(%s,%s,%s)"
        try:
            # if self.cursor.execute(sql, (item['author'], ",".join(item['tags']), item['text'])):
            if self.cursor.execute(sql, tuple(data.values())):
                self.connect.commit()
        except DropItem as e:
            print(DropItem('ERROR!'))
            self.connect.rollback()
        except IntegrityError:
            print("该课程courseURL已存在")
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
