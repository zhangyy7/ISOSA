#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""业务逻辑."""
import getpass
import hashlib
from db import inittables


class BaseUser(object):
    """用户基础功能."""

    def __init__(self):
        """初始化所需参数."""
        self.session = inittables.DBSession()
        self.user_info = {"islogin": False, "current_user": None}

    def login(self):
        """获取用户参数，调用login方法."""
        userid = input('请输入qq号码：>>>').strip()
        password = getpass.getpass('请输入密码：>>>').strip()
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        md5_pwd = md5.hexdigest()
        self._login(user=userid, password=md5_pwd)

    def _login(self, user, password):
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

    def _register(self, userid, name, password, sex, age, employment):
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
        self.session.commit()

    def register(self):
        """获取用户参数，调用_register方法."""
        qq = input('请输入您的QQ号码：>>>').strip()
        name = input('请输入您的姓名：>>>').strip()
        while True:
            password = getpass.getpass('请输入密码：>>>').strip()
            repassword = getpass.getpass('请再次输入密码：>>>').strip()
            if password == repassword:
                md5 = hashlib.md5()
                md5.update(password.encode('utf-8'))
                password = md5.hexdigest()
                break
            else:
                print("两次输入的密码不一致，请重新输入!")
                continue
        sex = input('请输入您的性别：【M-男|F-女】>>>').strip()
        age = input('请输入您的年龄：>>>').strip()
        employment = input('请输入您的职业：【s-学生|t-讲师】>>>').strip()
        self._register(
            userid=qq,
            name=name,
            password=password,
            sex=sex,
            age=age,
            employment=employment)

    def query_courses(self):
        """查询课程."""
        courses = self.session.query(inittables.Courses).all()
        return courses

    def query_classes(self):
        """查询班级."""
        pass

    @classmethod
    def auth(cls, func):
        """登录认证方法."""
        def decorator(*args, **kwargs):
            if not cls.user_info.get('islogin'):
                cls.login_api()
            return func(*args, **kwargs)
        return decorator


class Student(BaseUser):
    """学生类."""

    @BaseUser.auth
    def enroll(self, course_id):
        """报名方法."""
        apply_info = inittables.Apply(
            student_id=self.user_info["current_user"].qq,
            apply_course_id=course_id
        )
        self.session.add(apply_info)

    @BaseUser.auth
    def submit_homework(self):
        """交作业方法."""
        print("交作业")

    @BaseUser.auth
    def query_score(self):
        """查询成绩方法."""
        pass

    @BaseUser.auth
    def pay_tuition(self):
        """交学费方法."""


class Teacher(BaseUser):
    """讲师类."""

    pass


class Administrator(BaseUser):
    """管理员类."""

    pass


class ObjFactory(object):
    """对象工厂."""

    def __init__(self, employment):
        """根据职业创建对象."""
        if employment == 's':
            return Student()
        elif employment == 't':
            return Teacher()
        elif employment == 'a':
            return Administrator()
        else:
            raise ValueError('职业选择不正确！')
