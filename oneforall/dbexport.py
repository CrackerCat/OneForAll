#!/usr/bin/python3
# coding=utf-8

"""
OneForAll数据库导出模块

:copyright: Copyright (c) 2019, Jing Ling. All rights reserved.
:license: GNU General Public License v3.0, see LICENSE for more details.
"""

import fire
from common import database
from config import logger


def export(table, db=None, valid=None, path=None, format='xlsx', output=False):
    """
    OneForAll数据库导出模块

    Example:
        python dbexport.py --db result.db --table name --format csv --output False
        python dbexport.py --db result.db --table name --format csv --path= ./result.csv

    Note:
        参数valid可选值1，0，None，分别表示导出有效，无效，全部子域
        参数format可选格式：'csv', 'tsv', 'json', 'yaml', 'html', 'xls', 'xlsx', 'dbf', 'latex', 'ods'
        参数path为None会根据format参数和域名名称在项目结果目录生成相应文件

    :param str table:   要导出的表
    :param str db:      要导出的数据库路径(默认为results/result.sqlite3)
    :param int valid:   导出子域的有效性(默认None)
    :param str format:  导出格式(默认xlsx)
    :param str path:    导出路径(默认None)
    :param bool output: 是否将导出数据输出到终端(默认False)
    """
    db_conn = database.connect_db(db)
    if valid is None:
        rows = database.get_data(db_conn, table)
    elif isinstance(valid, int):
        rows = database.get_subdomain(db_conn, table, valid)
    else:
        rows = database.get_data(db_conn, table)  # 意外情况导出全部子域
    if output:
        print(rows.dataset)
    if not path:
        path = 'export.' + format
    logger.log('INFOR', f'正在将数据库中{table}表导出')
    try:
        with open(path, 'w') as file:
            file.write(rows.export(format))
            logger.log('INFOR', '成功完成导出')
            logger.log('INFOR', path)
    except TypeError:
        with open(path, 'wb') as file:
            file.write(rows.export(format))
            logger.log('INFOR', '成功完成导出')
            logger.log('INFOR', path)
    except Exception as e:
        logger.log('ERROR', e)


if __name__ == '__main__':
    fire.Fire(export)
