#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""连接数据库，初始化表."""
import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from conf import settings


# 初始化数据库连接
engine = create_engine(settings.database[settings.engine], encoding='utf-8')

# 创建映射表的基类
Base = declarative_base()

# 创建DBSession类
DBSession = sessionmaker(bind=engine)

# 创建映射到数据库表的映射类


class User(Base):
    """用户信息类."""

    __tablename__ = 'tf_user'

    qq = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    sex = Column(Enum('M', 'F'), default='M', nullable=False)
    age = Column(Integer, nullable=False)
    register_date = Column(
        DateTime, default=datetime.datetime.now(), nullable=False)
    status = Column(Integer, default=1)
    update_user = Column(Integer, ForeignKey('tf_user.qq'))
    update_time = Column(DateTime, default=datetime.datetime.now())


class Role(Base):
    """角色信息表映射类."""

    __tablename__ = 'tf_role'

    role_code = Column(String(8), primary_key=True)
    role_name = Column(String(32), nullable=False)
    update_time = Column(
        DateTime, default=datetime.datetime.now(), nullable=False)
    update_user = Column(Integer, ForeignKey('tf_user.qq'))


class Right(Base):
    """权限信息表映射."""

    __tablename__ = 'tf_right'

    right_code = Column(String(8), primary_key=True)
    right_name = Column(String(32), nullable=False)
    update_time = Column(DateTime, default=datetime.datetime.now())
    update_user = Column(Integer, ForeignKey('tf_user.qq'))


class RoleRight(Base):
    """角色与权限关系表."""

    __tablename__ = 'tr_role_right'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_code = Column(String(8), ForeignKey(
        'tf_role.role_code'), nullable=False)
    right_code = Column(String(8), ForeignKey(
        'tf_right.right_code'), nullable=False)
    update_user = Column(Integer, ForeignKey('tf_user.qq'))
    update_time = Column(
        DateTime, default=datetime.datetime.now(), nullable=False)


class UserRightORRole(Base):
    """用户权限关系表."""

    __tablename__ = 'tr_user_roleorright'

    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey('tf_user.qq'), nullable=False)
    right = Column(String(8), nullable=False)
    right_type = Column(Enum('1', '2'), nullable=False)
    update_time = Column(DateTime, default=datetime.datetime.now())
    update_user = Column(Integer, ForeignKey('tf_user.qq'))


class UserLoginLog(Base):
    """用户登录日志表."""

    __tablename__ = 'tl_login_log'

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey('tf_user.qq'))
    login_time = Column(DateTime, default=datetime.datetime.now())


class School(Base):
    """学校信息表."""

    __tablename__ = 'tf_school'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    create_date = Column(DateTime, default=datetime.datetime.now())
    update_time = Column(DateTime, default=datetime.datetime.now())


class Courses(Base):
    """课程信息表."""

    __tablename__ = 'tf_courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    create_date = Column(DateTime, default=datetime.datetime.now())
    update_time = Column(DateTime, default=datetime.datetime.now())

    timetable = relationship('TimeTable')


class TimeTable(Base):
    """课程表信息表."""

    __tablename__ = 'tf_timetable'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('tf_courses.id'))
    schedule = Column(String(32), nullable=False)
    content = Column(String(128), nullable=False)
    create_user = Column(Integer, ForeignKey('tf_user.qq'))
    create_date = Column(DateTime, default=datetime.datetime.now())
    update_user = Column(Integer, ForeignKey('tf_user.qq'))
    update_time = Column(DateTime, default=datetime.datetime.now())


class Classes(Base):
    """班级信息表."""

    __tablename__ = 'tf_classes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    course_id = Column(Integer, ForeignKey('tf_courses.id'))
    create_user = Column(Integer, ForeignKey('tf_user.qq'))
    create_date = Column(DateTime, default=datetime.datetime.now())
    update_user = Column(Integer, ForeignKey('tf_user.qq'))
    update_time = Column(DateTime, default=datetime.datetime.now())


class UserClassRef(Base):
    """用户班级关系表."""

    __tablename__ = 'tr_user_class'

    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey('tf_user.qq'))
    class_id = Column(Integer, ForeignKey('tf_classes.id'))
    update_user = Column(Integer, ForeignKey('tf_user.qq'))
    update_time = Column(DateTime, default=datetime.datetime.now())


class StudyRecord(Base):
    """学生上课记录表."""

    __tablename__ = 'tr_study_record'

    status_info = {1: "正常", 2: "迟到", 0: "缺勤"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    stuid = Column(Integer, ForeignKey('tf_user.qq'))
    timetable_id = Column(Integer, ForeignKey('tf_timetable,id'))
    status = Column(Integer, nullable=False)


# 创建所有定义好的表
Base.metadata.create_all(engine)
session = DBSession()
session.commit()
