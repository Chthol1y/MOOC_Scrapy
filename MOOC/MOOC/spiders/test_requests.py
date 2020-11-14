# #!/usr/bin/env python3
# # -*- coding: UTF-8 -*-
#
# import requests
# from pyquery import PyQuery as pq
# import os
#
# ## headers跟浏览器的设一样(伪造报头)
# headers = {
#     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/75.0.3770.90 Chrome/75.0.3770.90 Safari/537.36',
#     'cookie': 'EDUWEBDEVICE=2a699bca100a4bc6ba3267e6a946c106; WM_TID=282TTKi%2Ft2JFQAFFBEIpiuNVisSn%2B6BL; WM_NI=vfNOutD42da2vwKncHuYD54MKB5cCSyvx%2FNWnk9Dkp0ec%2Fksm1Y0UWJ9rjpAQsqPkjvpv4ynIxTLQpDcXfwcUjGNej1Q9Y4F9DB7wr8hOxjles5oEBQgoU2PBW5dcwtKcEg%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee92c421b6edf9a7e6348fb48ea7d54f968e9bbbf372e997b782ca48a393bab1b52af0fea7c3b92ab6ba82b0f88088ecfe85e43ab6a9858fe244b7878cd6b747899efb84c259bbaab8d0cd5daeb5f7a5ea7cf4bbadd0ea79afef97d1d85d8ae7be8bf34b93adbfb1ea62b6b0bad5fc668ba89cadd47c88bd9887f66997b689afe862f38ff7bab74efb9c8ed8f67afcb88199e968a7adfb90c84a93b9a1b6b15c8289fb85e27db895ada6e637e2a3; NTESSTUDYSI=506623b8face4ca29ef722e581bd3227; utm="eyJjIjoiIiwiY3QiOiIiLCJpIjoiIiwibSI6IiIsInMiOiIiLCJ0IjoiIn0=|aHR0cHM6Ly93d3cuZ29vZ2xlLmNvLmpwLw=="; hb_MA-A976-948FFA05E931_source=www.google.co.jp; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1562574902,1562585346,1562653862,1562677890; __utma=63145271.884186124.1562574903.1562662301.1562677890.6; __utmc=63145271; __utmz=63145271.1562677890.6.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1562678566; __utmb=63145271.12.9.1562678784603'
# }
#
# url = 'https://www.icourse163.org/web/j/mocCourseV2RpcBean.getCourseEvaluatePaginationByCourseIdOrTermId.rpc'
#
# ## csrfKey从浏览器拿，作用相当于SessionId
# ## courseid就是课程号，可用于遍历
# ## 剩下是页数之类的
# data = {
#     'csrfKey': '506623b8face4ca29ef722e581bd3227',
#     'courseId': '93001',
#     'pageIndex': '1',
#     'pageSize': '20',
#     'orderBy': '3'
# }
#
# resp = requests.post(url, data=data, headers=headers)
# doc = pq(resp.content)
# text = doc.text().encode('latin1').decode('utf-8')
# print(text)
