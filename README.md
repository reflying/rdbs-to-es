# 同步数据到ES

## Install

```sh
# 安装依赖
sudo pip install -r requirements.txt
# mysql需安装MySQLdb模块,oracle需安装cx_Oracle模块

# 复制并修改配置
cp settings.py.example.py settings.py
```

## 数据导入

相关demo

```sh
# 不做数据清洗
python rdb2es.py --index-name=tmp_org --doc-type=tmp_org   --docs-per-chunk=1000  --delete-index

# 数据清洗,对字段增减,转换,计算等
python rdb2es.py --index-name=tmp_org --doc-type=tmp_org   --docs-per-chunk=1000  --parser=test_tags --delete-index

# 定义es数据结构（mapping）
python rdb2es.py --index-name=tmp_org --doc-type=tmp_org   --docs-per-chunk=1000  --parser=test_tags  --mapping-file=es_mapping/example/example.json --delete-index

```

# ES字段类型
    https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html

# 常用的类型
字符串
    string
数字
    long, integer, short, byte, double, float
日期
    date
布尔型
    boolean
二进制
    binary

