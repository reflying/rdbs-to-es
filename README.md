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

# 数据清洗
python rdb2es.py --index-name=tmp_org --doc-type=tmp_org   --docs-per-chunk=1000  --parser=test_tags --delete-index

# 定义es数据结构（mapping）
python rdb2es.py --index-name=tmp_org --doc-type=tmp_org   --docs-per-chunk=1000  --parser=test_tags  --mapping-file=es_mapping/example/example.json --delete-index

```

