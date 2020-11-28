import scrapy
import re
import json
import datetime
import pandas as pd
from MOOC.items import classItem


def set_request_body(categoryChannelId=3002, page='1'):
    # categoryChannelId=3002 计算机学科
    return {
        'mocCourseQueryVo':
            '{{"categoryId":-1,"categoryChannelId":{arg1},"orderBy":0,"stats":30,"pageIndex":{arg2},"pageSize":20}}'.format(
                arg1=categoryChannelId, arg2=page)
    }


class MoocInfoSpider(scrapy.Spider):
    name = 'mooc_info'
    allowed_domains = ['www.icourse163.org']

    custom_settings = {
        'FEED_EXPORT_FIELDS': ['name', 'school', 'subscribe_num', 'endTime', 'startTime', 'teachers', 'courseURL',
                               'subject_type'],
        'ITEM_PIPELINES': {'MOOC.pipelines.Mysql_Pipeline': 400}
    }

    def __init__(self, channelId=42, channelName='Unknown'):
        super(MoocInfoSpider, self).__init__()
        print('channelId=', channelId, 'channelName=', channelName)
        # self.request_body={"categoryId":-1,"categoryChannelId":3002,"orderBy":0,"stats":30,"pageIndex":2,"pageSize":20}
        with open('cookie.txt', 'r', encoding='utf') as f:
            self.cookie = f.read()
        # subject_dict = pd.read_csv('subject_id.csv').set_index('subject_name')['subject_id'].to_dict()
        self.channelName = channelName
        self.channelId = channelId  # list(subject_dict.values())
        self.channelCount = 0
        # 计算机：3002，外语:2002，理学：2003，工学：3003，经济管理：3004，心理学：3007，文史哲：3005，艺术设计：3006，医药卫生：3008，教育教学：3010，法学：3009，
        # 农林园艺：3011，
        self.request_body = set_request_body(categoryChannelId=self.channelId, page='1')
        self.request_header = {
            # 'Host': 'www.icourse163.org',
            'Connection': 'keep-alive',
            # 'Content-Length': '112',
            'edu-script-token': re.findall("NTESSTUDYSI=(.*?);", self.cookie)[0],
            # TODO: Download Middleware process_response() 实现随机User-Agent
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.41',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Accept': '*/*',
            'Origin': 'https://www.icourse163.org',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': ' empty',
            'Referer': 'https://www.icourse163.org/channel/' + str(self.channelId) + '.htm',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
            'cookie': self.cookie,
        }
        self.search_ajax = 'https://www.icourse163.org/web/j/mocSearchBean.searchCourseCardByChannelAndCategoryId.rpc?csrfKey=' + \
                           re.findall("NTESSTUDYSI=(.*?);", self.cookie)[0]

    def start_requests(self):
        yield scrapy.FormRequest(url=self.search_ajax, method='POST', headers=self.request_header,
                                 meta={'dont_merge_cookies': True},
                                 formdata=self.request_body,
                                 callback=self.parse)

    def parse(self, response, **kwargs):
        # print(response.text)
        info_dict = json.loads(response.text)
        # print(info_dict)
        # *****************************当前页数信息*****************************
        # 当前页数：pageIndex    单页课程数量：pageSize     总页数：totalPageCount
        pageIndex = info_dict['result']['query']['pageIndex']
        print("Current Page: ", pageIndex)
        pageSize = info_dict['result']['query']['pageSize']
        totalCount = info_dict['result']['query']['totleCount']
        totalPageCount = info_dict['result']['query']['totlePageCount']
        nextPage = pageIndex + 1
        # ******************************页面内容*******************************
        # 课程名称  学校  参加人数    开课时间/结束时间    教师  链接
        for num in range(0, len(info_dict['result']['list'])):
            json_list = info_dict['result']['list'][num]
            if json_list['mocCourseBaseCardVo'] is None:
                continue
            name = json_list['mocCourseBaseCardVo']['name']
            school = json_list['mocCourseBaseCardVo']['schoolName']
            subscribe_num = json_list['mocCourseBaseCardVo']['enrollCount']
            if not isinstance(subscribe_num, int):
                print('isdigit', subscribe_num)
                subscribe_num = 0
            endTime = json_list['mocCourseBaseCardVo']['endTime']
            startTime = json_list['mocCourseBaseCardVo']['startTime']
            endTime = datetime.datetime.fromtimestamp(endTime / 1000)
            startTime = datetime.datetime.fromtimestamp(startTime / 1000)
            teachers = json_list['mocCourseBaseCardVo']['teacherName']
            # 通过courseId 和 生成课程页面URL
            courseId = json_list['id']
            school_shortName = json_list['mocCourseBaseCardVo']['schoolSN']
            courseURL = 'https://www.icourse163.org/course/{}-{}'.format(school_shortName, courseId)
            # 传输至 classItem
            item = classItem()
            item['name'] = name
            item['school'] = school
            item['subscribe_num'] = subscribe_num
            item['endTime'] = endTime
            item['startTime'] = startTime
            item['teachers'] = teachers
            item['courseURL'] = courseURL
            item['subject_type'] = self.channelName
            yield item
        if nextPage <= totalPageCount:
            # print('下一页： ', nextPage)
            yield scrapy.FormRequest(url=self.search_ajax, method='POST', headers=self.request_header,
                                     meta={'dont_merge_cookies': True},
                                     formdata=set_request_body(categoryChannelId=self.channelId, page=nextPage),
                                     callback=self.parse)
