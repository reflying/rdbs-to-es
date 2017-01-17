### 说明
> 支持从ORACLE,MYSQL数据库导出数据到ES中

### 安装

```sh
# 安装依赖
sudo pip install -r requirements.txt
# mysql需安装MySQLdb模块,oracle需安装cx_Oracle模块

```

### 配置
> 配置config目录下的json文件(默认为config.json)，修改ES连接地址和数据库连接信息，当sql语句为视图或join查询的时候，需要通过fields字段定义字段列表。
>
> 默认ES会将string类型字段做全文索引，比如name字段内容为“张三丰”，检索时通过“张”、“三”，“丰”能配置，直接检索“张三丰”时不能匹配；可以在config.json文件mapping段中关闭全文索引。

### 数据导入样例说明

```sh

# 参数说明
--index-name    索引名称，必填
--doc-type      索引下的文档名称，必填
--delete-index  如果索引已经存在，删除索引，可选
--user          数据库用户名，必填
--passwd        数据库密码，必填
--config-file   配置文件路径，必填
--parser        数据清洗的python脚本，可选

# 不做数据清洗
python rdb2es.py --index-name=tmp_org --doc-type=tmp_org   --user=oracle --passwd=test123 --config-file=config/config.json  --delete-index

# 数据清洗,对字段增减,转换,计算等
python rdb2es.py --index-name=tmp_org --doc-type=tmp_org  --user=oracle --passwd=test123 --config-file=config/config.json  --parser=test_tags --delete-index


```



### 常用的类型

##### 字符串:string
##### 数字:long, integer, short, byte, double, float
##### 日期:date
##### 布尔型:boolean
##### 二进制:binary



### ES字段类型汇总
> https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html

### 数据库配置样例

``` sh

    "db_oracle": {
        "desc": "oracle样例",
        "type": "oracle",
        "con_str": "192.168.0.113:1521/orcl",
        "sql": "select * from  table_name",
        "fields": [ ]
    },
    "db_mysql": {
        "desc": "mysql样例",
        "type": "mysql",
        "con_str": [
            "192.168.0.113:3306",
            "database_name",
            "utf8"
        ],
        "sql": "select a.userid,a.username,a.email,b.interest from  table_name_a a,table_name_b b where a.id = b.pid",
        "fields": [
            "userid",
            "username",
            "email",
            "interest"
        ]
    }

```
