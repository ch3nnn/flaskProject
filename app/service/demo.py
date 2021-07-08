# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/7/8 15:28


from flask import current_app

from app import db
from app.models.user import User


class DemoService:

    @classmethod
    def create(cls, **data):

        try:
            user = User(
                username=data["username"],
                password=User.set_password(data["password"])
            )
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return None
        else:
            return user

    @classmethod
    def get_user(cls, username):
        user = User.query.filter_by(username=username).first()
        return user
