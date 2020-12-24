# -*- coding: utf-8 -*-
# @Time : 2020/12/24 0024 17:53
# @Author : Chtholly
# @File : pyecharts_demo3.py
# @Software: PyCharm

from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
import pandas as pd
import pymysql
import MOOC.settings as settings

# 连接至Mysql
mysql_connection = pymysql.connect(host=settings.MYSQL_HOST,
                                   user=settings.MYSQL_USER,
                                   password=settings.MYSQL_PASSWD,
                                   db=settings.MYSQL_DBNAME,
                                   charset='utf8')

sql = "SELECT * FROM class_info"
# 获取数据库数据
sql_df = pd.read_sql(sql, mysql_connection)
# dataframe数据预处理
sql_df = sql_df[['school', 'name', 'classScore', 'scoreCount', 'courseURL']]
sql_df['school&name'] = sql_df['school'] + '-' + sql_df['name']
                        # + '-' + sql_df['scoreCount'] + '人评分' + \
                        # sql_df['courseURL']
sql_df['scoreCount'] = sql_df['scoreCount'].astype('int')
sql_df = sql_df[sql_df['scoreCount'] >= 2000]
sql_df = sql_df.sort_values(by='classScore', ascending=False).reset_index().head(30)

X_data = list(sql_df['school&name'])
Y_data = list(sql_df['classScore'])


def classScoreRank() -> Bar:
    bar = (
        Bar(init_opts=opts.InitOpts(width="500px", height='700px', theme=ThemeType.LIGHT))
        .add_xaxis(X_data)
        .add_yaxis(series_name='', y_axis=Y_data,
                   tooltip_opts=opts.TooltipOpts(
                       formatter=JsCode(
                           """function(param) { return [
                                       '学校&课程名 '  + ': ' + param.name,
                                       '评分: ' + param.data,
                                   ].join('<br/>') }"""
                       )
                   ),
        )
        .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts(title="评分人数2000人以上的课程评分排名(鼠标悬浮显示课程信息)"),
            xaxis_opts=opts.AxisOpts(),
            yaxis_opts=opts.AxisOpts(
                is_inverse=True,
                is_show=False,
            ),
            toolbox_opts=opts.ToolboxOpts(
                is_show=False,
            ),
            datazoom_opts=opts.DataZoomOpts(
                is_zoom_lock=True,
                range_start=94,
                range_end=100
            ),
        )
    )
    return bar


if __name__ == '__main__':
    bar_ = classScoreRank()
    bar_.page_title = "评分人数2000人以上的课程评分排名"
    bar_.render("评分人数2000人以上的课程评分排名.html")
