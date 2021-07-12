# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/7/8 17:26


from abc import ABC
from functools import wraps

import cerberus
from cerberus.errors import BasicErrorHandler
from flask import request

from app.common.result_code import ResultCode


class CustomErrorHandler(BasicErrorHandler, ABC):

    def __init__(self, tree=None, custom_messages=None):
        super(CustomErrorHandler, self).__init__(tree)
        self.custom_messages = custom_messages or {}

    def _format_message(self, field, error):
        tmp = self.custom_messages
        for x in error.schema_path:
            try:
                tmp = tmp[x]
            except KeyError:
                return super(CustomErrorHandler, self)._format_message(field, error)
        if isinstance(tmp, dict):  # if "unknown field"
            return super(CustomErrorHandler, self)._format_message(field, error)
        else:
            return tmp


class Validate:

    errors = list()

    @staticmethod
    def validateInputByName(name, rules, error_msg=None, default=''):
        """验证输入信息根据字段名

        :param name: string name
        :param rules: dict rules
        :param error_msg: string error_msg
        :param default:
        :return: response
        """
        # 不准使用error关键字作为请求参数,请求参数都会被格式化成string，无法使用int去验证
        if error_msg is None:
            error_msg = dict()
        if name == 'error':
            return {'msg': '不能使用error关键字作用请求参数', 'code': 0}
        v = cerberus.Validator(
            rules, error_handler=CustomErrorHandler(custom_messages=error_msg))
        # 这边修改成json格式接收参数
        try:
            requests = request.values()
        except TypeError:
            requests = request.get_json()
            requests = requests if requests else {}

        if name not in requests:
            requests[name] = default
        cookedReqVal = {name: requests[name]}
        if v.validate(cookedReqVal):  # validate
            return requests
        return {"error": v.errors}


def validator(name, method, rules, default=""):
    """验证装饰器

    :param name: 字段名
    :param rules: 规则
    :param default:
    :return: func|json
    """
    def wrappar(func):
        @wraps(func)
        def inner_wrappar(*args, **kwargs):
            if request.method in method:
                error = Validate.validateInputByName(name, {name: rules}, '', default)
                if 'error' in error:
                    return ResultCode.error(msg=str(error))
                if 'params' in kwargs.keys():
                    kwargs['params'][name] = error[name]
                    kwargs = kwargs['params']
                else:
                    kwargs = error
            return func(kwargs)

        return inner_wrappar

    return wrappar
