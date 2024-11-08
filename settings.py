#!/usr/bin/env python3
# ! -*- coding=utf-8 -*-
'''
**************************************************************
** @Create：2024/8/14 18:01
** @Author：Anonymous
** @Description：公共配置文件
**************************************************************
'''

import os
from datetime import timedelta


class Config(object):
    # 运行后端服务的的IP地址，开发环境建议用127.0.0.1
    SERVER_IP = '127.0.0.1'
    # 服务端口号，默认5000，修改此端口号后前端项目也要对应修改
    SERVER_PORT = 5000

    ''' session存储会话配置相关 '''
    # 如果采用session会话机制必须配置此字段,目的就是用于sessionid的加密，不配置会报错
    SECRET_KEY = "*(%#4sxcz(^(#$#8423"
    # 可选，配置 session 的 cookie 名称
    SESSION_COOKIE_NAME = 'test'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    # 在session中的session头添加的东西
    # SESSION_KEY_PREFIX='stu-'

    '''  数据库配置相关  '''
    HOST = '127.0.0.1'
    PORT = '3306'
    # 如果导入sql文件则不需要修改数据库名字，否则需要提前创建好自定义的数据库
    DATABASE = 'course_selection_manage'
    USERNAME = 'root'
    PASSWORD = 'ck87792017'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(
        username=USERNAME,
        password=PASSWORD, host=HOST,
        port=PORT, db=DATABASE)
    # 默认True，Flask-SQLAlchemy将会追踪对象的修改并且发送信号，这需要额外的内存，如果不需要可以禁用它
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 数据库调试模式使用为True，生产环境设置为False
    SQLALCHEMY_ECHO = False
    # 自动回收连接的秒数
    SQLALCHEMY_POOL_RECYCLE = 1

    # 目录相关
    ROOT_DIR = os.path.dirname(__file__)
    LOG_BASE_DIR = os.path.dirname(__file__) + "/logs/"

    # 避免json数据中文乱码
    JSON_AS_ASCII = False

    '''   邮件发送配置相关  '''
    # 邮箱服务器地址和端口号
    EMAIL_SERVER_ADDR = "smtp.qq.com"
    EMAIL_SERVER_PORT = 25
    # 邮件用户名和授权码
    EMAIL_USERNAME = "admin@qq.com"
    EMAIL_PASSWORD = "邮箱授权码"
    # 邮件发送调试日志级别(0--不打印交互信息，1--打印交互信息,默认为0)
    EMAIL_DEBUG_LEVEL = 0

    '''  图片上传配置相关  '''
    UPLOAD_FOLDER = os.path.dirname(__file__) + '/static/images/users/'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
