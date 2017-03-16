#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""业务逻辑."""

from db import inittables
from db.inittables import sessionmaker, engine


class BaseUser(object):
    """用户基础功能."""

    def __init__(self):
        """初始化所需参数."""
        self.session = sessionmaker(bind=engine)
        self.user_info = {"islogin": False, "current_user": None}

    def login(self, user, password):
        """用户登录方法."""
        user_info = self.session.query(
            inittables.User).filter(inittables.User.qq == user).all()
        real_user, real_password = user_info.qq, user_info.password
        if user == real_user and password == real_password:
            self.user_info["current_user"] = user
            self.user_info["islogin"] = True
            return {"islogin": True, "user_info": user_info}
        else:
            return {"islogin": False}

    def register(self, userid, password):


class Student(object):
    """学生"""
    pass
