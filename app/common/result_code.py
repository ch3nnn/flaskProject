# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/7/8 17:26

"""
基础控制器，封装一些基础方法
验证库https://cerberus.readthedocs.io/en/stable/index.html
"""

from flask import jsonify


class ResultCode:

    @classmethod
    def json(cls, body=None, msg=""):
        """
        * 返回Json数据
        * @param  dict body
        * @return json
        """
        if body is None:
            return jsonify({"code": 0, "msg": "无响应数据", "data": None})
        return cls.successData(data=body, msg=msg)

    @classmethod
    def error(cls, msg=''):
        """
        * 返回错误信息
        * @param  msg string
        * @return json
        """
        return jsonify({'code': 0, 'msg': msg, 'data': None})

    @classmethod
    def successData(cls, data=None, msg="请求成功"):
        """
        * 返回成功信息
        * @param  msg string
        * @return json
        """
        return jsonify({'code': 1, 'data': data, 'msg': msg})
