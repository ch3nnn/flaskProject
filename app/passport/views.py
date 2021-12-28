# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/7/8 10:18

from flask import Blueprint, request, session
from flask_login import login_required, login_user, logout_user

from app import cache
from app.common.result_code import ResultCode
from mq.MQSender import MQConnection, MQSender
from .service import Service

passport = Blueprint('passport', __name__, url_prefix='/api/user')


@passport.route("/register", methods=["POST"])
def register():
    """注册功能"""

    user = Service.insert(**request.json)
    if not user:
        return ResultCode.error("创建失败")
    return ResultCode.successData(data=user.to_dict, msg="创建成功")


@passport.route("/login", methods=["POST"])
def login():
    """登录功能"""

    username = request.json.get("username")
    password = request.json.get("password")
    user = Service.select_by_usr_pas(username=username, password=password)
    if user and user.check_password(user.password, password):
        login_user(user)
        cache.hset()
        cache.set(f"user_{user.id}", user.username)  # 缓存写入
        return ResultCode.successData(data=user.to_dict, msg="登录成功")
    return ResultCode.error(msg="用户名或密码错误")


@passport.route('/logout', methods=["GET"])
@login_required
def logout():
    """用户登出"""
    user_id = session.get("_user_id")
    username = cache.get(f"user_{user_id}")
    logout_user()

    sender = MQSender(MQConnection())
    print("@@@@@@@@@@@@@@@@@@@@@@@@测试发送@@@@@@@@@@@@@@")
    sender.send(exchange='test', routing_key='test', message=f"用户名: < {username} > 已登出")
    print("@@@@@@@@@@@@@@@@@@@@@@@@发送成功@@@@@@@@@@@@@@")
    return ResultCode.successData(msg='Logged out successfully!')

