#!E:\Program Files\Python35 python
# -*- coding: utf-8 -*-
# @Time : 2019/1/22 11:20
# @Author : Wulei# @Site : 
# @File : main.py
# @Software: PyCharm

import os, sys
from scrapy.cmdline import execute


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scray', 'crawl', 'judgment'])
