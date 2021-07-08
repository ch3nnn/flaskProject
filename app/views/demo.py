# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/7/8 10:18

from flask import Blueprint

from app import cache
from app.common.decorator import validator
from app.common.result_code import ResultCode
from app.service.demo import DemoService

demo = Blueprint('demo', __name__, url_prefix='/api')


@demo.route("/index", methods=["POST"])
@validator(name="username", rules={'required': True, 'type': 'string', 'minlength': 5, 'maxlength': 20})
@validator(name="password", rules={'required': True, 'type': 'string', 'minlength': 5, 'maxlength': 20})
def index(params):
    user = DemoService.create(**params)
    if not user:
        return ResultCode.error("创建失败")
    cache.set(f"user_{user.id}", user.username)
    return ResultCode.successData(data=user.to_dict, msg="创建成功")


@demo.route("/test/<user_id>", methods=["GET"])
def test(user_id):
    username = cache.get(f"user_{user_id}")
    user = DemoService.get_user(username)
    if not user:
        return ResultCode.error("未获取数据")
    return ResultCode.successData(user.to_dict)
