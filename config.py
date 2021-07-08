# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/7/8 09:45


import logging


# 基本配置信息
class Config(object):
    DEBUG = True

    # 数据库配置
    MYSQL_HOST = "localhost"
    MYSQL_PORT = "3306"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "123456"
    DATABASE = "test"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 数据库内容发送改变之后,自动提交

    # flask缓存配置
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "127.0.0.1"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_PASSWORD = "123456"
    CACHE_REDIS_DB = 0

    # 默认日志等级
    LEVEL = logging.DEBUG


# 开发模式
class DeveloperConfig(Config):
    pass


# 生产模式
class ProductConfig(Config):
    DEBUG = False
    LEVEL = logging.ERROR


# 测试模式
class TestingConfig(Config):
    pass


# 设置统一访问入口,使用config_dict
config_dict = {
    "develop": DeveloperConfig,
    "product": ProductConfig,
    "testing": TestingConfig
}
