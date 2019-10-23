# -*- coding: utf-8 -*-
import json
import math
from urllib import parse

import scrapy

from ..items import TencentItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['careers.tencent.com']

    keyword = input('请输入职位类型')
    keyword = parse.quote(keyword)

    one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?keyword={}&pageIndex={}&pageSize=10'
    two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?postId={}'
    # 内部源码，采用 dont_filter=True ，来处理 start_urls，所以之后可以再次使用该url
    start_urls = [one_url.format(keyword, 1)]

    def parse(self, response):
        count = json.loads(response.text)['Data']['Count']
        page = math.ceil(count / 10)
        for index in range(1, page + 1):
            url = self.one_url.format(self.keyword, index)
            print(url)
            yield scrapy.Request(url=url, callback=self.second_parse, dont_filter=False)

    def second_parse(self, response):
        json_obj = json.loads(response.text)
        print(response.url, len(json_obj['Data']['Posts']))
        for one in json_obj['Data']['Posts']:
            postid = one['PostId']
            url = self.two_url.format(postid)
            yield scrapy.Request(url=url, callback=self.third_parse, dont_filter=False)

    def third_parse(self, response):
        item = TencentItem()
        json_obj = json.loads(response.text)
        item['job_name'] = json_obj['Data']['RecruitPostName']
        item['job_type'] = json_obj['Data']['CategoryName']
        item['job_duty'] = json_obj['Data']['Responsibility']
        item['job_require'] = json_obj['Data']['Requirement']
        item['job_address'] = json_obj['Data']['LocationName']
        item['job_time'] = json_obj['Data']['LastUpdateTime']
        return item
