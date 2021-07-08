# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/7/8 13:35

from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class BaseModel:

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment="创建时间")
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow, comment="更新时间")

    @property
    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


class User(BaseModel, db.Model):
    __tablename__ = "user"
    __table_args__ = {'comment': '用户表'}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False, comment="用户名")
    password = db.Column(db.String(255), unique=True, nullable=False, comment="密码")

    # 设置密码
    @staticmethod
    def set_password(password):
        return generate_password_hash(str(password))

    # 校验密码
    @staticmethod
    def check_password(hash_password, password):
        return check_password_hash(hash_password, password)
