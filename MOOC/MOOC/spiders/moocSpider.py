import scrapy
import re
import json
import datetime
from MOOC.items import classItem


def set_request_body(classname=None, page='1'):
    """
    生成request body 供访问接口使用
    :param classname: 搜索关键词
    :param page: 页数
    :return: request body 键值对
    """
    return {
        'mocCourseQueryVo':
            '{{"keyword":{arg1},"pageIndex":{arg2},"highlight":true,"orderBy":0,"stats":30,"pageSize":20}}'.format(
                arg1=classname, arg2=page)
    }


class moocSpider(scrapy.Spider):
    name = 'moocSpider'
    allowed_domains = ['www.icourse163.org']
    # start_urls = ['http://www.icourse163.org/']

    # 自定义scrapy settings内容
    custom_settings = {
        'FEED_EXPORT_FIELDS': ['name', 'school', 'subscribe_num', 'endTime', 'startTime', 'teachers', 'courseURL'],
        'DOWNLOADER_MIDDLEWARES': {
            'MOOC.middlewares.RandomUserAgentMiddleware': 543,
        }
    }

    def __init__(self, classname=None):
        super(moocSpider, self).__init__()

        with open('cookie.txt', 'r', encoding='utf') as f:
            self.cookie = f.read()
        self.classname = classname
        self.request_body = set_request_body(classname=classname, page='1')
        self.request_header = {
            # 'Host': 'www.icourse163.org',
            'Connection': 'keep-alive',
            # 'Content-Length': '112',
            'edu-script-token': re.findall("NTESSTUDYSI=(.*?);", self.cookie)[0],
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.41',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Origin': 'https://www.icourse163.org',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': ' empty',
            'Referer': 'https://www.icourse163.org/search.htm?search=' + classname + '#/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
            'cookie': self.cookie,
        }
        self.search_ajax = 'https://www.icourse163.org/web/j/mocSearchBean.searchCourse.rpc?csrfKey=' + \
                           re.findall("NTESSTUDYSI=(.*?);", self.cookie)[0]
        self.search_url = 'https://www.icourse163.org/search.htm?search={class_name}#/'.format(class_name=classname)

    def start_requests(self):
        print(self.cookie)
        yield scrapy.FormRequest(url=self.search_ajax, method='POST', headers=self.request_header,
                                 meta={'dont_merge_cookies': True},
                                 formdata=self.request_body,
                                 callback=self.parse)

    def parse(self, response, **kwargs):
        """
        读取接口json数据并解析
        """
        info_dict = json.loads(response.text)
        # *****************************当前页数信息*****************************
        # 当前页数：pageIndex    单页课程数量：pageSize     总页数：totalPageCount
        pageIndex = info_dict['result']['query']['pageIndex']
        pageSize = info_dict['result']['query']['pageSize']
        totalPageCount = info_dict['result']['query']['totlePageCount']
        nextPage = pageIndex + 1
        flag = 1
        print("Current Page: ", pageIndex)
        # ******************************页面内容*******************************
        # 课程名称  学校  参加人数    开课时间/结束时间    教师  链接
        for num in range(0, pageSize):
            json_list = info_dict['result']['list'][num]
            # 忽略缺少相关信息的课程，此类课程多为广告和培训班
            if json_list['mocCourseCard'] is None:
                continue
            name = re.sub(r'({##)|(##})', '', json_list['highlightName'])
            # 如果课程名已跟搜索关键词无关，则停止爬取
            if not re.findall(self.classname, name, flags=re.IGNORECASE):
                print('已无相关课程')
                flag = 0
                break

            # 大学名称、选课人数、教师姓名爬取
            school = json_list['highlightUniversity']
            subscribe_num = json_list['mocCourseCard']['mocCourseCardDto']['termPanel']['enrollCount']
            teachers = json_list['mocCourseCard']['highlightTeacherNames']

            # 默认获取的是UNIX时间（POSIX时间）通过datetime标准库进行转换
            endTime = json_list['mocCourseCard']['mocCourseCardDto']['termPanel']['endTime']
            startTime = json_list['mocCourseCard']['mocCourseCardDto']['termPanel']['startTime']
            endTime = datetime.datetime.fromtimestamp(endTime / 1000)
            startTime = datetime.datetime.fromtimestamp(startTime / 1000)

            # 通过courseId 和 生成课程页面URL
            courseId = json_list['courseId']
            school_shortName = json_list['mocCourseCard']['mocCourseCardDto']['schoolPanel']['shortName']
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
            yield item

        if nextPage <= totalPageCount and flag == 1:
            # 通过修改request body内页面数据，实现翻页效果
            yield scrapy.FormRequest(url=self.search_ajax, method='POST', headers=self.request_header,
                                     meta={'dont_merge_cookies': True},
                                     formdata=set_request_body(classname=self.classname, page=nextPage),
                                     callback=self.parse)
