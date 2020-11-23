# -*- coding: utf-8 -*-
# @Time : 2020/11/22 0022 17:33
# @Author : Chtholly
# @File : main2.py
# @Software: PyCharm

import os
import pandas as pd


def get_all_subject_info():
    subject_dict = pd.read_csv('subject_id.csv').set_index('subject_name')['subject_id'].to_dict()
    channelId_list = list(subject_dict.values())
    channelName_list = list(subject_dict.keys())
    print(channelId_list)
    print(channelName_list)
    channelCount = 0

    while channelCount < len(channelId_list):
        print('爬取 '+channelName_list[channelCount]+' 课程信息')
        os.system('scrapy crawl mooc_info -o all_class_{arg1}.csv -a channelId={arg2}'.format(
            arg1=channelName_list[channelCount], arg2=channelId_list[channelCount])
        )
        channelCount += 1


if __name__ == '__main__':
    get_all_subject_info()