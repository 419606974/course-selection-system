#!/usr/bin/env python3
# ! -*- coding=utf-8 -*-
'''
**************************************************************
** @Create：2024/8/15 8:30
** @Author：Anonymous
** @Description：封装数据库操作
**************************************************************
'''

import pymysql
from loguru import logger
from settings import Config

import pymysql
from loguru import logger
from settings import Config


class DbHandle:
    def __init__(self):
        self.host = Config.HOST
        self.port = int(Config.PORT)
        self.user = Config.USERNAME
        self.passwd = Config.PASSWORD
        self.database = Config.DATABASE
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                        database=self.database, connect_timeout=30)
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            return self.conn
        except Exception as e:
            logger.error("connect to {0} fail, error info: {1}", self.host, e)
            self.conn = None
            self.cursor = None

    def execute_sql(self, sql_cmd, params=None):
        try:
            with self.connect() as conn:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    if params:
                        cursor.execute(sql_cmd, params)
                    else:
                        cursor.execute(sql_cmd)
                    conn.commit()
                    return cursor
        except Exception as error:
            self.conn.rollback()
            logger.error("mysql error: {0}", error)
            return None
        # finally:
        #     if self.cursor:
        #         self.cursor.close()
        #     if self.conn:
        #         self.conn.close()
