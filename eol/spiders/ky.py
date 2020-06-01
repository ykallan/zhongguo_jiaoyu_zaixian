# -*- coding: utf-8 -*-
import scrapy
import json
import re
from ..items import EolItem


class KySpider(scrapy.Spider):
    name = 'ky'
    allowed_domains = ['eol.cn']
    start_urls = ['http://eol.cn/']
    start_url = 'https://souky.eol.cn/web/school/school_search?act=do&format=json&province=&pro_school_type=&first_rate=0&flag_yjxk=0&flag_985=0&flag_211=0&flag_score=0&flag_zdsys=0&flag_yjsy=0&keyword=&page={}'
    tiaoji_ajax = 'https://souky.eol.cn/web/statics/schoolnewslist?classid=4&school_id={}'
    detail_url = 'https://souky.eol.cn'

    def start_requests(self):
        # for i in range(1,114):
        for i in range(1, 114):
            yield scrapy.Request(url=self.start_url.format(i),callback=self.parse)

    def parse(self, response):
        resp = json.loads(response.text)['message']['data']
        print(type(resp))
        for school in resp:
            yield scrapy.Request(url=self.tiaoji_ajax.format(school['school_id']), callback=self.each_school)


    def each_school(self, response):
        print(response.text)
        detial_ruls = re.findall(r'a href="(.*?)">', response.text)
        for url in detial_ruls:
            print(url)
            yield scrapy.Request(url=self.detail_url+url, callback=self.detial_info)



    def detial_info(self, response):
        item = EolItem()
        # print(response.text)
        title = response.xpath('//p[@class="title"]/text()').extract_first()
        content = response.xpath('//div[@class="guidemain_txt_y"]/p/text()').extract()
        # print(content)
        con = ' '.join([con for con in content])
        # print(con)

        item['title'] = title
        item['con'] = con
        yield item