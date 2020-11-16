import scrapy
import re


class DownloadSpider(scrapy.Spider):
    name = 'downloadSpider'
    allowed_domains = ['https://www.icourse163.org/']

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69",
    }

    def __init__(self, url=None):
        super(DownloadSpider, self).__init__()
        self.url = url

    def start_requests(self):
        yield scrapy.Request(url=self.url, method='GET', callback=self.parse)

    def parse(self, response, **kwargs):
        # #g-body > script:nth-child(3)
        # script_info = response.css('#g-body > script:nth-child(3)::text').extract_first()
        # print(script_info)
        # print("---------------------------------------------------------------")

        # print(termInfoList)
        # print(response.css('#g-body > script:nth-child(3)::text').extract_first())
        script_info = response.css('#g-body > script:nth-child(3)::text').extract_first()
        script_info = str(script_info)
        script_info = script_info.replace('\n', '')
        termInfoList = re.findall(r'window.termInfoList = \[(.*?)\];', script_info, flags=re.M)
        # print(script_info)
        print("---------------------------------------------------------------")
        print(termInfoList)
