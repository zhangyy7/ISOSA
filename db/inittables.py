#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""连接数据库，初始化表."""

from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from conf import settings

# 初始化数据库连接
engine = create_engine(settings.database[settings.engine], encoding='utf-8')

# 创建映射表的基类
Base = declarative_base()


class UserLoginLog(Base):
    """用户登录日志表."""

    __tablename__ = 'tl_login_log'

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey('tf_user.qq'))
    login_time = Column(DateTime, server_default=func.now())


class Apply(Base):
    """学生报名申请表."""

    __tablename__ = 'tr_student_apply'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('tf_user.qq'))
    apply_course_id = Column(Integer, ForeignKey('tf_courses.id'))
    apply_date = Column(DateTime, server_default=func.now())
    pay_tag = Column(Enum('0', '1'), server_default='0')
    users = relationship('User', foreign_keys=[student_id], backref=backref('applys'))


class UserInfo(Base):
    """用户信息类."""

    __tablename__ = 'tf_user'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    qq = Column("qq", Integer, unique=True)
    role_id = Column("role_id", Integer, ForeignKey("tf_role.id"))
    name = Column("name", String(32), nullable=False)
    sex = Column("sex", Enum('M', 'F'), server_default='M')
    age = Column("age", Integer, nullable=False)
    password = Column("password", String(64), nullable=False)
    status = Column("status", String(1), server_default='1')
    register_date = Column("register_date", DateTime, server_default=func.now())
    update_time = Column("update_time", DateTime, server_default=func.now())
    update_user = Column("update_user_id", Integer, ForeignKey("tf_user.id"))

    # 添加关系属性（关联到role_id外键上）
    roles = relationship('RoleInfo', foreign_keys=[role_id])


class RoleInfo(Base):
    """角色信息表映射类."""

    __tablename__ = 'tf_role'
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), unique=True, nullable=False)

    # 添加关系属性（关联到UserInfo.role_id属性上）
    users = relationship('UserInfo', foreign_keys="UserInfo.role_id")


class SchoolInfo(Base):
    """学校信息表."""

    __tablename__ = 'tf_school'
    __table_args = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), unique=True, nullable=False)
    headmaster_id = Column("headmaster_id", Integer, ForeignKey("tf_user.id"))
    update_time = Column(DateTime, server_default=func.now())

    # 添加关系属性（关联到headmater_id外键上）
    headmaster = relationship("UserInfo", foreign_keys="SchoolInfo.headmaster_id")


class Courses(Base):
    """课程信息表."""

    __tablename__ = 'tf_courses'
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(64), unique=True, nullable=False)
    create_user_id = Column("create_user_id", Integer, ForeignKey("tf_user.id"))
    price = Column("price", Integer, nullable=False)
    cycle = Column("cycle", Integer)


class TimeTable(Base):
    """课程表信息表."""

    __tablename__ = 'tf_timetable'
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('tf_courses.id'))
    schedule = Column(String(32), nullable=False)
    content = Column(String(128), nullable=False)
    create_user = Column(Integer)
    create_date = Column(DateTime, server_default=func.now())
    update_user = Column(Integer)
    update_time = Column(DateTime, server_default=func.now())

    courses = relationship('Courses', foreign_keys=[course_id], backref=backref('timetables'))


class Classes(Base):
    """班级信息表."""

    __tablename__ = 'tf_classes'
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), unique=True, nullable=False)
    course_id = Column(Integer, ForeignKey('tf_courses.id'))
    teacher_id = Column(Integer, ForeignKey("tf_user.id"))
    create_user = Column(Integer, ForeignKey("tf_user.id"))
    create_date = Column(DateTime, server_default=func.now())
    update_user = Column(Integer, ForeignKey("tf_user.id"))
    update_time = Column(DateTime, server_default=func.now())
    courses = relationship('Courses', foreign_keys=[course_id, ])
    teachers = relationship("UserInfo", foreign_keys=[teacher_id, ])


class ClassesStudentRef(Base):
    """班级与学员关系表."""

    __tablename__ = "tr_classes_student_ref"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    classes_id = Column("classes_id", Integer, ForeignKey("tf_classes.id"))
    student_id = Column("student_id", Integer, ForeignKey("tf_user.id"))


# 创建所有定义好的表
Base.metadata.create_all(engine)
