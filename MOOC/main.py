# -*- coding: utf-8 -*-
# @Time : 2020/11/9 0009 10:37
# @Author : Chtholly
# @File : main.py
# @Software: PyCharm

import scrapy
from scrapy.cmdline import execute
import os
import time
import pandas
import numpy as np
from prettytable import PrettyTable, FRAME


def search_course(file_name, file_type):
    # 调用moocSpider爬取指定关键词的课程搜索结果
    currentTime = time.strftime('%Y.%m.%d_%H.%M.%S', time.localtime(time.time()))

    if os.path.exists(filename + filetype):
        os.rename(file_name + file_type, file_name + currentTime + file_type)

    os.system('scrapy crawl moocSpider -a classname={0} -o {1}'.format(course_name, filename + filetype))
    # 'scrapy crawl moocSpiderSpider -a classname=高等数学 -o course_information.csv'


def display_result(file_name, file_type):
    # 读取搜索页面爬取数据
    search_result = pandas.read_csv(file_name + file_type)
    search_result = search_result.rename(
        dict(zip(np.arange(0, search_result.shape[0]), np.arange(1, search_result.shape[0] + 1))))
    # 按照参加人数排序
    search_result['subscribe_num'] = search_result['subscribe_num'].apply(int)
    search_result = search_result.sort_values(by='subscribe_num', ascending=False)
    search_result = search_result.reset_index()
    search_result.index += 1
    # 转换为 PrettyTable 表格数据
    table = PrettyTable(['  ', '序号', '课程名', '开设院校', '参加人数', '结束时间', '开始时间', '授课老师', '课程地址'])
    table.align = 'l'  # 左对齐
    table.vrules = FRAME
    table.vertical_char = ' '
    table.align["授课老师"] = 'c'
    table.align["开设院校"] = 'c'

    for i in np.arange(1, search_result.shape[0] + 1):
        table.add_row(
            ['  ', i, search_result.loc[i]['name'], search_result.loc[i]['school'],
             search_result.loc[i]['subscribe_num'],
             search_result.loc[i]['endTime'], search_result.loc[i]['startTime'], search_result.loc[i]['teachers'],
             search_result.loc[i]['courseURL']])
    # 输出构造完毕的table
    print(table)


if __name__ == '__main__':
    course_name = input("请输入要查询的课程关键词：")
    filename = 'course_information'
    filetype = '.csv'

    search_course(filename, filetype)
    display_result(filename, filetype)
