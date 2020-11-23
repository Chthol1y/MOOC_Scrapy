# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoocItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class classItem(scrapy.Item):
    name = scrapy.Field()
    school = scrapy.Field()
    subscribe_num = scrapy.Field()
    endTime = scrapy.Field()
    startTime = scrapy.Field()
    teachers = scrapy.Field()
    courseURL = scrapy.Field()


class subjectItem(scrapy.Item):
    subject_name = scrapy.Field()
    subject_id = scrapy.Field()
