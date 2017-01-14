#!/usr/bin/python
# -*- coding: UTF-8 -*-
#


import json
import sys
from threading import local
import datetime
import traceback
import click
from joblib import Parallel, delayed
from pyelasticsearch import ElasticSearch
from pyelasticsearch import bulk_chunks
from pyelasticsearch import ElasticHttpNotFoundError
from retrying import retry
from importlib import import_module
import time
import os
import csv
from settings import *


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  # oracle中文编码

reload(sys)
sys.setdefaultencoding('utf-8')


__version__ = '1.0.1'
thread_local = local()

# 数据解析器的目录
PARSER_PATH = "parse"

# 时间格式化
ISOTIMEFORMAT='%Y-%m-%d %X'

def echo(message, quiet=False):

    if not quiet:
        click.echo(message)

def documents_from_file(es,collection,quiet,parser_fun):


    cur = collection.cursor()
    result = cur.execute(DB['sql'])

    # 获取数据表的列名
    if len(DB['fields']) == 0 :
        try:
            fields = [i[0].lower() for i in cur.description]
        except:
            fields = []
    fields_len = len(fields)

    if   DB['type'] == "mysql":
        result = cur.fetchall()

    def all_docs():
        count = 0
        for row in result:
            try:
                doc = {}
                for index, v in enumerate(row):
                    if fields_len == 0 :
                        doc['f' + str(index)] = v
                    else:
                        doc[fields[index]] = v
                count += 1
                if count % 5000 == 0:
                    echo('Sent documents: ' + str(count), quiet)

                if parser_fun is not None:
                    doc = parser_fun.row_parser(doc)

                if doc:
                    yield es.index_op(doc)
            except:
                traceback.print_exc()
        cur.close()
        collection.close()

    return all_docs


@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_attempt_number=10)
def local_bulk(host, index_name, doc_type, chunk):

    if not hasattr(thread_local, 'es'):
        thread_local.es = ElasticSearch(host)

    thread_local.es.bulk(chunk, index=index_name, doc_type=doc_type)


def perform_bulk_index(host, index_name, doc_type, doc_fetch, docs_per_chunk, bytes_per_chunk, parallel):
    Parallel(n_jobs=parallel)(
        delayed(local_bulk)(host, index_name, doc_type, chunk)
        for chunk in bulk_chunks(doc_fetch(),
                                 docs_per_chunk=docs_per_chunk,
                                 bytes_per_chunk=bytes_per_chunk))

@click.command()
@click.option('--index-name', required=True,
              help='Index name to load data into     ')
@click.option('--doc-type', required=True,
              help='The document type (like user_records)')
@click.option('--mapping-file', required=False,
              help='JSON mapping file for index')
@click.option('--settings-file', required=False,
              help='Settings file for es index')
@click.option('--host', default=ES_CONF['host'], required=False,
              help='The Elasticsearch host (%s)' % ES_CONF['host'])
@click.option('--docs-per-chunk', default=5000, required=False,
              help='The documents per chunk to upload (5000)')
@click.option('--bytes-per-chunk', default=100000, required=False,
              help='The bytes per chunk to upload (100000)')
@click.option('--parallel', default=1, required=False,
              help='Parallel uploads to send at once, defaults to 1')
@click.option('--delete-index', is_flag=True, required=False,
              help='Delete existing index if it exists')
@click.option('--quiet', is_flag=True, required=False,
              help='Minimize console output')
@click.option('--parser', default=None, required=False,
              help='格式解释器, 对应parse目录下')

@click.version_option(version=__version__, )
def cli(index_name, delete_index, mapping_file, settings_file, doc_type, host,docs_per_chunk, bytes_per_chunk, parallel, quiet, parser):

    echo('Using host: ' + host, quiet)
    es = ElasticSearch(host)

    if DB['type'] == "oracle":
        db = import_module('cx_Oracle')
        collection = db.connect(DB['con_str'])
    else:
        db = import_module('MySQLdb')
        collection = db.connect(DB['con_str'][0],DB['con_str'][1],DB['con_str'][2],DB['con_str'][3],charset=DB['con_str'][4])

    if delete_index:   # 删除索引
        try:
            stamp = 0
            es.delete_index(index_name)
            echo('Deleted: ' + index_name, quiet)
        except ElasticHttpNotFoundError:
            echo('Index ' + index_name + ' not found, nothing to delete', quiet)

    try:
        if settings_file:
            with open(settings_file, 'r') as f:
                settings_json = json.loads(f.read())
            es.create_index(index_name, settings=settings_json)
        else:
            es.create_index(index_name)
        echo('Created new index: ' + index_name, quiet)
    except Exception:
        echo('Index ' + index_name + ' already exists', quiet)

    echo('Using document type: ' + doc_type, quiet)
    if mapping_file:
        echo('Applying mapping from: ' + mapping_file, quiet)
        with open(mapping_file) as f:
            mapping = json.loads(f.read())
        es.put_mapping(index_name, doc_type, mapping)

    parser_fun = None
    if parser is not None:
        # 加载解释函数
        parser_fun = import_module(PARSER_PATH + '.' + parser)

    documents = documents_from_file(es, collection,quiet, parser_fun)

    perform_bulk_index(host, index_name, doc_type, documents, docs_per_chunk,bytes_per_chunk, parallel)

if __name__ == "__main__":
    print  "start:" +time.strftime(ISOTIMEFORMAT, time.localtime())
    cli()
    print  "end:" + time.strftime(ISOTIMEFORMAT, time.localtime())+'/n all records import complete.'
    
