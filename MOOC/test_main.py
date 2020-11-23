# -*- coding: utf-8 -*-
# @Time : 2020/11/15 0015 15:22
# @Author : Chtholly
# @File : test_main.py
# @Software: PyCharm

import scrapy
from scrapy.cmdline import execute

# execute(['scrapy', 'crawl', 'downloadSpider', '-a', 'url=https://www.icourse163.org/course/BIT-268001'])
execute('scrapy crawl mooc_info -o total_cs_class.csv'.split())
# execute('scrapy crawl mooc_subject -o subject_id.csv'.split())
