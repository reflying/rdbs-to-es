#!/usr/bin/python
# -*- coding: UTF-8 -*-
#

from datetime import date
import datetime
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')
# 当前日期
now = date.today()

weekday = ["1周一", "2周二", "3周三", "4周四", "5周五", "6周六", "7周日"]


def row_parser(row):
    '''格式解释
    @param dict row 其中一行, 格式：{'field1': 'value1', 'field2': 'value2'}
    @return 格式：{'field1': 'value1', 'field2': 'value2'}
      '''

    if 'au_create_time' in row and row['au_create_time'] is not None:
        t1 = datetime.datetime.strptime(row['au_create_time'], '%Y-%m-%d %H:%M:%S')
        row['process_time'] = (t1-t).days
        try:
            row['au_create_time'] = row['au_create_time'].replace(" ","T")+'+08:00'
        except:
            row['au_create_time'] = '2088-02-01T23:59:59+08:00'
    else:
        row['process_time'] = -1

    return row
