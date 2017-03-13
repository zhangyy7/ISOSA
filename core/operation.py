#! /usr/bin/env python
# -*- coding:utf-8 -*-
from db.inittables import session
from db import inittables


class BaseUser(object):
    """用户基础功能."""

    def __init__(self):
        """初始化所需参数."""
        self.session = session

    def login(self, user, password):
        """用户登录方法."""
        user_info = self.session.query(
            inittables.User).filter(inittables.User.qq == user).all()
        real_user, real_password = user_info.qq, user_info.password
        if user == real_user and password == real_password:
            return {"islogin": True, "user_info": user_info}
        else:
            return {"islogin": False}


class Student(object):
    """学生"""
