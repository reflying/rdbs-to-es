#!/usr/bin/python
# -*- coding: UTF-8 -*-

# es config
ES_CONF = {
    'host': 'http://121.199.49.215:9200'
}

# 数据库连接参数

DB =  {
    'type':'oracle',
    'con_str':'V_DG/V_DG@192.168.3.188:1521/orcl',
    'sql_type':'single',
    'sql':'select * from  tmp_org',
    'fields':[]
}

# oracle样例

DB_ORACLE =  {
    'type':'oracle',
    'con_str':'username/password@192.168.0.113:1521/orcl',
    'sql_type':'single',
    'sql':'select * from  table_name',
    'fields':[]
}

# mysql样例

DB_MYSQL =  {
    'type':'mysql',
    'con_str':["192.168.0.113:3306","username","password","database_name","utf8")],
    'sql_type':'join',
    'sql':'select a.userid,a.username,a.email,b.interest from  table_name_a a,table_name_b b where a.id = b.pid',
    'fields':['userid','username','email','interest']
}

