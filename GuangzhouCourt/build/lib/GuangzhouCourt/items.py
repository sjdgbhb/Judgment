# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GuangzhoucourtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JudgmentItem(scrapy.Item):
    judgment_name = scrapy.Field() # 文书名
    format_CourName = scrapy.Field() # 法院名
    format_DocType = scrapy.Field() #　文书类型
    format_CaseNum = scrapy.Field() # 案号
    format_Paragraph = scrapy.Field() # 正文段落
    format_Person = scrapy.Field() # 审判相关人员
    format_Date = scrapy.Field() # 判决日期
    # 文件下载
    file_urls = scrapy.Field() # 文件下载链接
    files = scrapy.Field() # 文件下载完成后会往里面写相关的信息