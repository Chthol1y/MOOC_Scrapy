# -*- coding: utf-8 -*-
# @Time : 2020/11/30 0030 18:06
# @Author : Chtholly
# @File : pyecharts_demo.py
# @Software: PyCharm

import jieba
import numpy as np
import pandas as pd
import pymysql
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Page, Pie, WordCloud
from pyecharts.globals import ThemeType

import MOOC.settings as settings
from app import subject_all_class

# 连接至Mysql
mysql_connection = pymysql.connect(host=settings.MYSQL_HOST,
                                   user=settings.MYSQL_USER,
                                   password=settings.MYSQL_PASSWD,
                                   db=settings.MYSQL_DBNAME,
                                   charset='utf8')

sql = "SELECT * FROM class_info"
sql_df = pd.read_sql(sql, mysql_connection)
sort_by_num = sql_df.sort_values(by='subscribeNum', ascending=False).reset_index()
sort_by_num['school&name'] = sort_by_num['school'] + '-' + sort_by_num['name']
sort_by_num['subscribeNum'] = list(map(int, list(sort_by_num['subscribeNum'])))

# 选择选课人数排名前25的课程
sort_by_num = sort_by_num.head(25)

# 获得所有学科名
subject_dict = pd.read_csv('subject_id.csv').set_index('subject_name')['subject_id'].to_dict()
subjectName_list = list(subject_dict.keys())

# 用于jieba分词使用的过滤词汇
fp = open('./stopwords.dat', "r", encoding="utf-8")
stopwords = fp.readlines()
fp.close()
for i in range(len(stopwords)):
    stopwords[i] = stopwords[i].rstrip("\n")


# 选择选课人数排名前25柱状图
def course_selection_ranking() -> Grid:
    c = (
        Bar(init_opts=opts.InitOpts(width="40%", theme=ThemeType.LIGHT))
        .add_xaxis(list(sort_by_num['school&name']))
        .add_yaxis('', list(sort_by_num['subscribeNum']))
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="选课人数排名TOP25"),
            yaxis_opts=opts.AxisOpts(is_inverse=True),
        )
    )
    g = (
        Grid(init_opts=opts.InitOpts(width="40%", theme=ThemeType.LIGHT))
        .add(c, grid_opts=opts.GridOpts(pos_left="250"))
    )
    return g


def add_bar():
    bar_list = []
    for name in subjectName_list:
        df = subject_all_class(name)
        bar = Bar(init_opts=opts.InitOpts(width="40%", theme=ThemeType.LIGHT))
        bar.add_xaxis(list(df['x']))
        bar.add_yaxis('开课数量', list(df['y']))
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title="计算机学科开课数量排名"),
        )
        bar_list.append(bar)
    return bar_list


# 计算机学科开课数量排名柱状图（全部学科在pyecharts_demo2中）
def class_sum_by_subject() -> Bar:
    return add_bar()[2]


# 各学科课程占比饼状图
def subject_pie() -> Pie:
    # sql_df['subjectType']
    subjectType_sum = sql_df['subjectType'].value_counts()
    subject_num = list(subjectType_sum)
    subject_name = list(subjectType_sum.index)
    pie_data = [list(z) for z in zip(subject_name, subject_num)]
    p = (
        Pie(init_opts=opts.InitOpts(width="40%", theme=ThemeType.LIGHT))
        .add(
            "课程数量",
            pie_data,
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="各学科课程占比饼状图"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return p


# 课程名分词后生成词云
def word_cloud() -> WordCloud:
    input_list = []
    total_seg = np.array([])
    for s in list(sql_df['name']):
        seg_list = list(jieba.cut_for_search(s))
        for seg in seg_list:
            total_seg = np.append(total_seg, seg)

    for item in np.unique(total_seg):
        if np.sum(total_seg == item) >= 30 and (item not in stopwords) and (item != ' '):
            input_list.append((item, str(np.sum(total_seg == item))))

    c = (
        WordCloud(init_opts=opts.InitOpts(width="40%", theme=ThemeType.LIGHT))
        .add("词云分析", input_list)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="词云分析"
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )
    return c


# 对整体HTML页面进行排版
def page_simple_layout():
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        course_selection_ranking(),
        class_sum_by_subject(),
        subject_pie(),
        word_cloud(),
    )
    page.page_title = "MOOC当前开放课程可视化"
    page.render("当前全部开放课程可视化.html")


if __name__ == "__main__":
    page_simple_layout()
