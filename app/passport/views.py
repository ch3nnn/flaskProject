# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/7/8 10:18

from flask import Blueprint, request
from flask_login import login_required, login_user, logout_user

from app import cache
from app.common.decorator import validator
from app.common.result_code import ResultCode
from .service import Service

passport = Blueprint('passport', __name__, url_prefix='/api')


@passport.route("/register", methods=["POST"])
@validator(name="username", method=["POST"], rules={'required': True, 'type': 'string', 'minlength': 5, 'maxlength': 20})
@validator(name="password", method=["POST"], rules={'required': True, 'type': 'string', 'minlength': 5, 'maxlength': 20})
def register(params):
    user = Service.create(**params)
    if not user:
        return ResultCode.error("创建失败")
    cache.set(f"user_{user.id}", user.username)
    return ResultCode.successData(data=user.to_dict, msg="创建成功")


@passport.route("/login", methods=["GET", "POST"])
@validator(name="username", method=["POST"], rules={'required': True, 'type': 'string', 'minlength': 5, 'maxlength': 20})
@validator(name="password", method=["POST"], rules={'required': True, 'type': 'string', 'minlength': 5, 'maxlength': 20})
def login(params):
    if request.method == "POST":
        user = Service.query_user(username=params["username"])
        if user and user.check_password(user.password, params["password"]):
            login_user(user)
            return ResultCode.successData(data=user.to_dict, msg="登录成功")
        return ResultCode.error(msg="用户名或密码错误")
    elif request.method == "GET":
        return ResultCode.successData(msg="重新登录")


@passport.route('/logout', methods=["GET"])
@login_required
def logout():
    """用户登出"""
    logout_user()
    return ResultCode.successData(msg='Logged out successfully!')

