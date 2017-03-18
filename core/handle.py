#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""业务逻辑."""

from db import inittables


class BaseUser(object):
    """用户基础功能."""

    def __init__(self):
        """初始化所需参数."""
        self.session = inittables.DBSession()
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

    def register(self, userid, name, password, sex, age, employment):
        """用户注册方法."""
        userinfo = inittables.User(
            qq=userid,
            name=name,
            password=password,
            sex=sex,
            age=age,
            employment=employment
        )
        self.session.add(userinfo)
        self.session.commit()\


    def query_courses(self):
        """查询课程."""
        pass

    def query_classes(self):
        """查询班级."""
        pass


class Student(BaseUser):
    """学生类."""

    def enroll(self):
        """报名方法."""
        pass

    def submit_homework(self):
        """交作业方法."""
        pass

    def query_score(self):
        """查询成绩方法."""
        pass

    def pay_tuition(self):
        """交学费方法."""


class Teacher(BaseUser):
    """讲师类."""
