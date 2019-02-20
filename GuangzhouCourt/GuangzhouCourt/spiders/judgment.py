# -*- coding: utf-8 -*-

import re
import scrapy
from GuangzhouCourt.items import JudgmentItem


class JudgmentSpider(scrapy.Spider):
    name = 'judgment'
    allowed_domains = ['ssfw.gzcourt.gov.cn:8080']
    start_urls = [
        'http://ssfw.gzcourt.gov.cn:8080/webapp/area/gz/cpws/cpws_data.jsp?yzmCxPage=1&jarq1={}&jarq2={}&currentPage={}&lx={}'.format(
            '1900-01-01_', '2019-01-24_', '1', 'ms'),
        # 'http://ssfw.gzcourt.gov.cn:8080/webapp/area/gz/cpws/cpws_data.jsp?yzmCxPage=1&jarq1={}&jarq2={}&currentPage={}&lx={}'.format(
        #     '1900-01-01_', '2019-01-22_', '1', 'xs'),
        # 'http://ssfw.gzcourt.gov.cn:8080/webapp/area/gz/cpws/cpws_data.jsp?yzmCxPage=1&jarq1={}&jarq2={}&currentPage={}&lx={}'.format(
        #     '1900-01-01_', '2019-01-22_', '1', 'zx'),
        # 'http://ssfw.gzcourt.gov.cn:8080/webapp/area/gz/cpws/cpws_data.jsp?yzmCxPage=1&jarq1={}&jarq2={}&currentPage={}&lx={}'.format(
        #     '1900-01-01_', '2019-01-22_', '1', 'pc'),
      ] # 民事、刑事、执行、国家赔偿

    def parse(self, response):
        '''
        解析列表页，获取详情页url
        :param response:
        :return:
        '''
        # 获取文书名
        item_name = response.xpath("//td[contains(@class,'bg')]/text()").extract() # 条目名
        item_list = []
        for item in item_name:
            item = item.strip()
            if item:
                if not re.findall('^\d*?$', item):
                    item_list.append(item)
        # 条目列表分成三个一小组，以便连接
        judgment_list = [list(i) for i in zip(*(iter(item_list),) *3)]
        count = len(item_list) % 3
        judgment_list.append(item_list[-count:]) if count != 0 else judgment_list
        judgment_name_list = [] # 拥有相等长度子列表的文书名表
        for judgment in judgment_list:
            judgment_name_list.append('_'.join(judgment) + '.doc')
        # 获取文书url参数
        item_actionIcon = response.xpath("//img[@class='actionIcon']/@onclick").extract() # 条目链接参数
        judgment_args_list = [] # 文书链接参数
        for actionIcon in item_actionIcon:
            args = re.findall(r"'(\d*?)'", actionIcon)
            judgment_args_list.append(args)
        # 详情页
        for judgment_args in judgment_args_list:
            meta = {'judgment_name': judgment_name_list[judgment_args_list.index(judgment_args)]} # 与文书链接相对应的文书名
            detail_url = 'http://ssfw.gzcourt.gov.cn:8080/webapp/area/gz/cpws/cpws_view.jsp?lsh={}&xh={}'.format(judgment_args[0],judgment_args[1])
            yield scrapy.Request(url=detail_url, meta=meta, callback=self.parse_detail, dont_filter=True)  # 提交详情页下载任务，由self.parse_detail解析
        # 列表页
        if response.url in self.start_urls: # 第一次请求列表页计算总页数
            html = response.text
            page_nums = re.findall(r'共搜索到\d*份文书.*?(\d*)页.*?每页\d*条', html)
            if page_nums:
                page_nums = page_nums[0]
                for page_num in range(2, int(page_nums) + 1):
                    page_num_args = 'currentPage=' + str(page_num) # 页码参数
                    items_url = re.sub(r'currentPage=(\d*)', page_num_args, response.url) # 列表页url
                    yield scrapy.Request(url=items_url, callback=self.parse, dont_filter=True) # 提交列表页下载任务，由self.parse解析

    def parse_detail(self, response):
        '''
        解析详情页
        :param response:
        :return:
        '''
        item = JudgmentItem()
        judgment_name = response.meta.get('judgment_name')
        item['judgment_name'] = judgment_name
        if response.headers.get('Content-Disposition'): # url可以直接下载文书
            item['file_urls'] = [response.url]
        else: # url只能解析文书
            format_CourName = response.xpath("//div[@class='format_CourtName']").extract()
            format_DocType = response.xpath("//div[@class='format_DocType']").extract()
            format_CaseNum = response.xpath("//div[@class='format_CaseNum']").extract()
            format_Paragraph = response.xpath("//div[@class='format_Paragraph']").extract()
            format_Person = response.xpath("//div[@class='format_Person']").extract()
            format_Date = response.xpath("//div[@class='format_Date']").extract()
            item['format_CourName'] = format_CourName
            item['format_DocType'] = format_DocType
            item['format_CaseNum'] = format_CaseNum
            item['format_Paragraph'] = format_Paragraph
            item['format_Person'] = format_Person
            item['format_Date'] = format_Date
        yield item