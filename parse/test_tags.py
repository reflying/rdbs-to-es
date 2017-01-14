#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# 
#
# age => current date - birth date
# life_cycle => close date - op acct date
#



from datetime import date
import datetime
import time
import sys
from snownlp import SnowNLP
from libs.extract_tags import TFIDF
from format_dongguan_subject import parse_subject
from extract_department import  extract_department
from extract_location import extract_location

reload(sys)
sys.setdefaultencoding('utf8')
# 当前日期
now = date.today()

weekday = ["1周一", "2周二", "3周三", "4周四", "5周五", "6周六", "7周日"]


def row_parser(row,city):
    '''csv格式解释
    @param dict row 其中一行, 格式：{'field1': 'value1', 'field2': 'value2'}
    @return 格式：{'field1': 'value1', 'field2': 'value2'}
    '''


    if row['title'] is None:
        row['title'] = ''
    if row['content'] is None:
        row['content'] = ''
        row['content_sentiments'] = 0
    else:
        # 情感得分
        s = SnowNLP(row['content'])
        row['content_sentiments'] = s.sentiments

    tags = TFIDF(row['title']+row['content'], topK=100)
    row['content_tags'] = u";".join(tags)

    if 'au_content' in row and row['au_content'] is not None:
        tags = TFIDF(row['au_content'], topK=100)
        row['au_content_tags'] = u";".join(tags)
    if 'au_reply_content' in row and row['au_reply_content'] is not None:
        tags = TFIDF(row['au_reply_content'], topK=100)
        row['au_reply_content_tags'] = u";".join(tags)

    # 主题分类
    row['appeal_subject'] = parse_subject(row['root_name'].decode("utf8"),row['title'].decode("utf8"),row['content'].decode("utf8"))

    # 部门处理
    row['department'] = extract_department(row,city)

    # 镇区处理
    row['district'] = extract_location(row, city)

    # 计算周几

    row['process_time'] = extract_department(row['root_name'], city)

    t = datetime.datetime.strptime(row['create_time'],'%Y-%m-%d %H:%M:%S')
    row['weekday'] = weekday[t.weekday()]
    row['hour'] = t.hour
    row['create_time'] = str(t).replace(" ", "T") + '+08:00'

    row['event_addr_not_analyzed'] = row['event_addr']
    row['title_not_analyzed'] = row['title']

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
