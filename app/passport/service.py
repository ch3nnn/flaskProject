# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/7/8 15:28


from flask import current_app

from app import db
from app.passport.models import User


class BaseModel:

    @classmethod
    def transaction(cls, func):
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
    def create(cls, **data):
        password = User.set_password(data["password"])
        return User(username=data["username"], password=password)

    @classmethod
    def query_user(cls, **kwargs):
        return User.query.filter_by(**kwargs).first()
