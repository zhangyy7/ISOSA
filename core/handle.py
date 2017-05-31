#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""业务逻辑."""
import getpass
import hashlib
from db import inittables


class Util(object):
    """工具类."""

    @staticmethod
    def auth(func):
        """登录认证方法."""

        def decorator(self, *args, **kwargs):
            """装饰器方法."""
            if not self.user_info:
                self.login()
            return func(self, *args, **kwargs)
        return decorator


class BaseUser(object):
    """用户基础功能."""

    def __init__(self):
        """初始化所需参数."""
        self.session = inittables.DBSession()
        self.user_info = {}

    def login(self):
        """获取用户参数，调用login方法."""
        count = 0
        while not self.user_info and count < 3:
            print("调用登录方法")
            userid = input('请输入qq号码：>>>').strip()
            password = getpass.getpass('请输入密码：>>>').strip()
            md5 = hashlib.md5()
            md5.update(password.encode('utf-8'))
            md5_pwd = md5.hexdigest()
            self._login(user=userid, password=md5_pwd)
            count += 1
        else:
            exit(1)

    def _login(self, user, password):
        """用户登录方法."""
        user_info = self.session.query(
            inittables.User).filter(inittables.User.qq == user).first()
        if user_info:
            real_user, real_password = user_info.qq, user_info.password
            if user == str(real_user) and password == real_password:
                self.user_info["current_user"] = user
                self.user_info["islogin"] = True
            else:
                print("账号或密码不正确！")
        else:
            print("账号或密码不正确！")

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
        classes = self.session.query(inittables.Classes).all()
        return classes


class Student(BaseUser):
    """学生类."""

    @Util.auth
    def enroll(self, course_id):
        """报名方法."""
        apply_info = inittables.Apply(
            student_id=self.user_info["current_user"].qq,
            apply_course_id=course_id
        )
        self.session.add(apply_info)

    @Util.auth
    def submit_homework(self):
        """交作业方法."""
        print("交作业")

    @Util.auth
    def query_score(self):
        """查询成绩方法."""
        pass

    @Util.auth
    def pay_tuition(self):
        """交学费方法."""
        pass

    @Util.auth
    def query_self_apply_status(self):
        """查询自己的申请状态."""
        qq = self.user_info['current_user'].qq
        apply_record = self.session.query(inittables.Apply).filter(
            inittables.Apply.student_id == qq).first()
        return apply_record


class Teacher(BaseUser):
    """讲师类."""

    def create_classes(self, name, course_name):
        """创建班级."""
        course_id = self.session.query(inittables.Courses).filter(
            inittables.Courses.name == course_name).first()
        classobj = inittables.Classes(
            name=name,
            course_id=course_id
        )
        self.session.add(classobj)
        self.session.commit()

    def add_student(self):
        """根据学生QQ号把学生加入班级."""
        record = self._query_apply()
        return record

    def _query_apply(self):
        """查询报名申请记录."""
        pass

    def all_approve(self, *qq):
        """全部审批通过."""
        pass

    def create_classrecord(self, course_id):
        """创建指定班级的上课记录."""

        # 根据班级ID查询出所有学员
        self.session.query(inittables.user_class_ref)


class Administrator(BaseUser):
    """管理员类."""

    def create_course(self, name):
        """创建课程方法."""
        course_obj = inittables.Courses(
            name=name
        )
        self.session.add(course_obj)
        self.session.commit()


class ObjFactory(object):
    """对象工厂."""

    def __init__(self, employment):
        """根据职业创建对象."""
        self.employment = employment

    def factory(self):
        """根据职业创建对象."""
        if self.employment == 's':
            return Student()
        elif self.employment == 't':
            return Teacher()
        elif self.employment == 'a':
            return Administrator()
        else:
            raise ValueError('职业不正确！')
