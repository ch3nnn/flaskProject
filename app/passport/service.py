# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/7/8 15:28


from flask import current_app

from app import db
from app.passport.models import User


class BaseModel:

    @classmethod
    def transaction(cls, func):
        """数据库提交事务"""
        def inner(*args, **kwargs):
            try:
                obj = func(*args, **kwargs)
                db.session.add(obj)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(e)
                return None
            else:
                return obj
        return inner

    @classmethod
    def create(cls, *args, **kwargs):
        pass


class Service:

    @classmethod
    @BaseModel.transaction
    def insert(cls, **data):
        """创建用户"""
        password = User.set_password(data["password"])
        return User(username=data["username"], password=password)

    @classmethod
    def select_by_usr_pas(cls, username, password):
        """查询用户校验密码"""
        user = User.query.filter_by(username=username).first()
        if user:
            if user.check_password(user.password, password):
                return user
            return None
        return None
