#!E:\Program Files\Python35 python
# -*- coding: utf-8 -*-
# @Time : 2019/1/22 16:11
# @Author : Wulei# @Site : 
# @File : download.py
# @Software: PyCharm

import re
import requests


url1 = 'http://ssfw.gzcourt.gov.cn:8080/webapp/area/gz/cpws/cpws_view.jsp?lsh=255100000241130&xh=0000'
url2 = 'http://ssfw.gzcourt.gov.cn:8080/webapp/area/gz/cpws/cpws_view.jsp?lsh=255100000009202&xh=0000'
r = requests.get(url2)
pass