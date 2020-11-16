# -*- coding: utf-8 -*-
# @Time : 2020/11/15 0015 15:22
# @Author : Chtholly
# @File : test_main.py
# @Software: PyCharm

import scrapy
from scrapy.cmdline import execute

execute(['scrapy', 'crawl', 'downloadSpider', '-a', 'url=https://www.icourse163.org/course/BIT-268001'])
# print('!!!!!!!!!!!!')
# https://www.icourse163.org/course/BIT-268001
# https://www.icourse163.org/learn/BIT-268001?tid=1461953449
