# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/7/8 09:24


# 权限模块 https://github.com/raddevon/flask-permissions
# from flask_permissions.core import Permissions

import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy

from config import config_dict

# 创建对象db
db = SQLAlchemy()
cache = Cache()

# 定义redis_store
redis_store = None


# 工厂方法,根据不同的参数,创建不同环境下的app对象
def create_app(config_name):
    app = Flask(__name__)

    # 根据传入的config_name获取到对应的配置类
    config = config_dict[config_name]

    # 日志方法调用
    log_file(config.LEVEL)

    # 加载配置类的中配置信息
    app.config.from_object(config)

    # 初始化组件
    db.init_app(app)
    cache.init_app(app)

    # 注册首页蓝图对象
    from app.views.demo import demo
    app.register_blueprint(demo)

    # 全局异常捕获
    @app.errorhandler(Exception)
    def error_handler(e):
        data = {
            "code": 0,
            "msg": str(e),
            "data": None
        }
        return jsonify(data)

    return app


# 日志文件,作用:用来记录程序的运行过程,比如:调试信息,接口访问信息,异常信息
def log_file(level):
    # 设置日志的记录等级,设置日志等级: 常见等级有:DEBUG < INFO < WARING < ERROR < FATAL(CRITICAL)
    logging.basicConfig(level=level)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件编号
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)
