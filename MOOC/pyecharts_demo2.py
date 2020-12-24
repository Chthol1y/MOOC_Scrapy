# -*- coding: utf-8 -*-
# @Time : 2020/11/30 0030 19:43
# @Author : Chtholly
# @File : pyecharts_demo2.py
# @Software: PyCharm
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Tab

from app import subject_all_class

subject_dict = pd.read_csv('subject_id.csv').set_index('subject_name')['subject_id'].to_dict()
subjectName_list = list(subject_dict.keys())


def add_bar():
    bar_list = []
    for name in subjectName_list:
        df = subject_all_class(name)
        bar = Bar(init_opts=opts.InitOpts(width="1200px"))
        bar.add_xaxis(list(df['x']))
        bar.add_yaxis('开课数量', list(df['y']))
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title="各学科开课数量排名"),
            yaxis_opts=opts.AxisOpts(is_inverse=True),
            datazoom_opts=[opts.DataZoomOpts(range_start=0,range_end=40), opts.DataZoomOpts(type_="inside")],
        )
        bar_list.append(bar)
    return bar_list


def class_sum_by_subject() -> Tab:
    tab_ = Tab()
    tab_content = add_bar()

    for content, name in zip(tab_content, subjectName_list):
        print(content)
        print(name)
        tab_.add(content, name)

    return tab_


if __name__ == '__main__':
    tab = class_sum_by_subject()
    tab.page_title = "各学科开课数量排名"
    tab.render("各学科开课数量排名.html")
