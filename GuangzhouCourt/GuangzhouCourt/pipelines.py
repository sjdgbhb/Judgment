# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.utils.project import get_project_settings


settings = get_project_settings() # 用于读取settings.py的参数


class GuangzhoucourtPipeline(object):
    def process_item(self, item, spider):
        return item


class JudgmentFilesPipeline(FilesPipeline):
    '''
    url文件下载
    '''
    def get_media_requests(self, item, info):
        meta = {'judgment_name': item.get('judgment_name')} # 文件名
        for file_url in item.get('file_urls', []):
            yield scrapy.Request(file_url, meta=meta)

    def item_completed(self, results, item, info):
        if 'files' in item:
            item['files'] = [x for ok, x in results if ok]
        return item

    def file_path(self, request, response=None, info=None):
        '''
        文件名
        :param request:
        :param response:
        :param info:
        :return:
        '''
        return request.meta.get('judgment_name')


class JudgmentPipeline(object):
    '''
    写入文件下载
    '''
    def process_item(self, item, spider):
        if not item.get('file_urls'):
            item_value_serialization = {key: str(value) + '\r\n' for key, value in item.items()}
            file = settings.get('FILES_STORE') + '\\' + item.get('judgment_name')
            with open(file, 'w' ,encoding='utf-8') as f:
                f.write(item_value_serialization.get('format_CourName'))
                f.write(item_value_serialization.get('format_DocType'))
                f.write(item_value_serialization.get('format_CaseNum'))
                f.write(item_value_serialization.get('format_Paragraph'))
                f.write(item_value_serialization.get('format_Person'))
                f.write(item_value_serialization.get('format_Date'))
        return item