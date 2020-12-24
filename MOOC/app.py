# -*- coding: utf-8 -*-
# @Time : 2020/11/23 0023 19:28
# @Author : Chtholly
# @File : app.py
# @Software: PyCharm

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pymysql
import MOOC.settings as settings
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[
    'https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/4.5.3/css/bootstrap.min.css'])


# ---------------read data---------------
def subject_all_class(subject_name):
    """
    读取指定学科的学校开课排名
    :param subject_name: 学科名, source from subject_id.csv
    :return:
    """
    source_df = pd.read_csv('../cache/all_class_{}.csv'.format(subject_name))
    source = source_df['school'].value_counts()

    source_X = list(source.index)
    source_Y = list(map(int, list(source.values)))
    df = pd.DataFrame({'x': source_X, 'y': source_Y})
    return df


subject_dict = pd.read_csv('subject_id.csv').set_index('subject_name')['subject_id'].to_dict()
subjectName_list = list(subject_dict.keys())

# options data for dcc.Dropdown components
options = []
for i in range(len(subject_dict)):
    temp = dict([('label', subjectName_list[i]), ('value', i)])
    options.append(temp)

# get data for sort the subscribe number of class from Mysql server
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
# select top 50 class for the Figure 1
sort_by_num = sort_by_num.head(50)
mysql_connection.close()

# ---------------Other settings---------------
colors = {
    # 'background': '#111111',
    # 'text': '#7FDBFF'
}

# ---------------App layout---------------
# vertical bar fig of Figure 1
vertical_bar_fig = px.bar(sort_by_num, x=list(sort_by_num['subscribeNum']), y=list(sort_by_num['school&name']),
                          hover_data=['teachers', 'school', 'courseURL', 'subjectType'],
                          labels={'x': 'X：参与人数', 'y': ''},
                          orientation='h')
vertical_bar_fig.update_layout(
    yaxis={'categoryorder': 'array', 'categoryarray': list(sort_by_num['school&name'])[::-1]},
)

# navbar
navbar = dbc.Navbar(
    [
        # Use row and col to control vertical alignment of logo / brand
        dbc.Row(
            [
                dbc.Col(
                    html.Img(src='https://images.plot.ly/logo/new-branding/plotly-logomark.png', height="30px"),
                    width=2
                ),
                dbc.Col(
                    dbc.NavbarBrand("中国大学MOOC 爬虫数据分析"), width=3),
            ],
            align="center",
            no_gutters=True,
        ),
    ],
    color="dark",
    dark=True,
)

# Figure 1
figure_1 = html.Div(id='vertical_bar',
                    children=[
                        dcc.Graph(figure=vertical_bar_fig, style={'height': 1000})],
                    )
# Figure 2
figure_2 = html.Div(id='university_class_sum_by_subject_',
                    children=[
                        dcc.Graph(id='bar_graph', style={'width': 1000}),
                    ])
# Figure 3
figure_3 = html.Div(id='subject_percentage_figure',
                    children=[
                        dcc.Graph(
                            figure=px.pie(sql_df, names='subjectType'), style={'height': 555})
                    ])

# HTML start
app.layout = html.Div(children=[
    navbar,
    html.H1("基于dash plotly与bootstrap的爬虫数据可视化", style={'text-align': 'center'}),
    html.H5("093118120 肖利东", style={'text-align': 'center'}),
    html.Br(),
    dbc.Row([
        dbc.Col([html.P(children=['选课人数排名'])], width={'size': 3, 'offset': 2}),
        dbc.Col(
            dbc.Row([
                dbc.Col(html.P(children=['每个学科下的大学开课数量排名'], style={'display': 'inline-block'}), width={'size': 5}),
                # dcc.Dropdown components
                dbc.Col(
                    html.Div(id='dropdown_1', children=[
                        dcc.Dropdown(id='subject_select', options=options, placeholder="选择一类学科", value=2)],
                             style={"width": "75%", 'display': 'inline-block'})
                )],
                no_gutters=True
            ),
            width={'size': 6, 'offset': 0.7},
        )
    ]),
    dbc.Row([
        # Figure 1 选课人数排名
        dbc.Col(figure_1, md={'size': 4, 'offset': 1}),
        dbc.Col(children=[
            # Figure 2 每个学科下的大学开课数量排名
            dbc.Row([figure_2]),
            # Figure 3 MOOC所有学科课程占比饼状图
            dbc.Row(
                dbc.Col(figure_3, md={'offset': 1})
            )
        ],
            md={'size': 6, 'offset': 0.7}
        ),

    ],
        no_gutters=False,
    ),
])


# ---------------app callback---------------
@app.callback(
    Output('bar_graph', 'figure'),
    Input('subject_select', 'value')
)
# TODO 点击条形图跳转至课程
def update_figure(selected_value):
    figure_df = subject_all_class(subjectName_list[selected_value])
    fig = px.bar(figure_df, x='x', y='y', labels={'x': '', 'y': 'Y：开课数量'})
    fig.update_layout(transition_duration=1)
    return fig


# ---------------Run Server---------------
if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(host='10.18.44.11', debug=True)
