import scrapy
import re
from MOOC.items import subjectItem


class MoocSubjectSpider(scrapy.Spider):
    name = 'mooc_subject'
    allowed_domains = ['www.icourse163.org']

    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'ROBOTSTXT_OBEY': False,
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf_8_sig',
        'CONCURRENT_REQUESTS': 100,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
        'CONCURRENT_REQUESTS_PER_IP': 100,
        'COOKIES_ENABLED': False,
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.58',
        },
        'FEED_EXPORT_FIELDS': ['subject_id', 'subject_name']
    }

    def __init__(self):
        super(MoocSubjectSpider, self).__init__()
        self.base_url = 'https://www.icourse163.org/channel/{}.htm'
        self.count = 1

    def start_requests(self):
        yield scrapy.Request(url=self.base_url.format(self.count), callback=self.parse)

    def parse(self, response, **kwargs):
        title_source = response.css('title::text').getall()[0]
        title = re.findall('(.*?)_中国大学MOOC\(慕课\)', title_source)[0]
        if title != '频道页':
            item = subjectItem()
            item['subject_name'] = title
            item['subject_id'] = self.count
            print(item)
            yield item
        if self.count < 50000:
            self.count += 1

        yield scrapy.Request(url=self.base_url.format(self.count), callback=self.parse)
