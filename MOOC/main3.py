# -*- coding: utf-8 -*-
# @Time : 2020/11/15 0015 15:22
# @Author : Chtholly
# @File : main3.py
# @Software: PyCharm

import scrapy
from scrapy.cmdline import execute
execute('scrapy crawl mooc_subject -o subject_id.csv'.split())
