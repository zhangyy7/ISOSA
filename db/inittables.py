#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""连接数据库，初始化表."""

from sqlalchemy import create_engine, Table
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from conf import settings


# 初始化数据库连接
engine = create_engine(settings.database[settings.engine], encoding='utf-8')

# 创建映射表的基类
Base = declarative_base()

# 创建DBSession类
DBSession = sessionmaker(bind=engine)

# 创建映射到数据库表的映射类


# 用户权限关系表
user_right_ref = Table(
    'tr_user_right', Base.metadata,
    Column('user_id', Integer, ForeignKey('tf_user.qq')),
    Column('right_code', String(8), ForeignKey('tf_right.right_code')),
    Column('updata_time', DateTime, server_default=func.now())
)


# 用户角色关系表
user_role_ref = Table(
    'tr_user_role', Base.metadata,
    Column('user_id', Integer, ForeignKey('tf_user.qq')),
    Column('role_code', String(8), ForeignKey('tf_role.role_code')),
    Column('updata_time', DateTime, server_default=func.now())
)


# 角色与权限关系表
role_right_ref = Table(
    'tr_role_right', Base.metadata,
    Column('role_code', String(8), ForeignKey('tf_role.role_code')),
    Column('right_code', String(8), ForeignKey('tf_right.right_code')),
    Column('updata_time', DateTime, server_default=func.now())
)


# 用户上课记录表
study_record_ref = Table(
    'tf_study_record', Base.metadata,
    Column('user_id', Integer, ForeignKey('tf_user.qq')),
    Column('timetable_id', Integer, ForeignKey('tf_timetable.id')),
    Column('status', String(1), server_default='1'),
    Column('updata_time', DateTime, server_default=func.now())
)


# 用户班级关系表
user_class_ref = Table(
    'tr_user_class', Base.metadata,
    Column('user_id', Integer, ForeignKey('tf_user.qq')),
    Column('class_id', Integer, ForeignKey('tf_classes.id')),
    Column('updata_time', DateTime, server_default=func.now())
)


class UserLoginLog(Base):
    """用户登录日志表."""

    __tablename__ = 'tl_login_log'

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey('tf_user.qq'))
    login_time = Column(DateTime, server_default=func.now())


class User(Base):
    """用户信息类."""

    __tablename__ = 'tf_user'

    id = Column(Integer, primary_key=True)
    qq = Column(Integer, unique=True)
    name = Column(String(32), nullable=False)
    password = Column(String(64), nullable=False)
    sex = Column(Enum('M', 'F'), server_default='M')
    age = Column(Integer, nullable=False)
    employment = Column(Enum('s', 't'), nullable=False)
    register_date = Column(DateTime, server_default=func.now())
    status = Column(String(1), server_default='1')
    create_user = Column(Integer)
    create_date = Column(DateTime, server_default=func.now())
    update_user = Column(Integer)
    update_time = Column(DateTime, server_default=func.now())

    roles = relationship('Role', secondary=user_role_ref,
                         backref=backref('users'))
    rights = relationship('Right', secondary=user_right_ref,
                          backref=backref('users'))


class Role(Base):
    """角色信息表映射类."""

    __tablename__ = 'tf_role'

    id = Column(Integer, primary_key=True)
    role_code = Column(String(8), unique=True, nullable=False)
    role_name = Column(String(32), unique=True, nullable=False)
    create_user = Column(Integer)
    create_date = Column(DateTime, server_default=func.now())
    update_user = Column(Integer)
    update_time = Column(DateTime, server_default=func.now())

    rights = relationship('Right', secondary=role_right_ref,
                          backref=backref('roles'))


class Right(Base):
    """权限信息表映射."""

    __tablename__ = 'tf_right'

    id = Column(Integer, primary_key=True)
    right_code = Column(String(8), unique=True, nullable=False)
    right_name = Column(String(32), unique=True, nullable=False)
    create_user = Column(Integer)
    create_date = Column(DateTime, server_default=func.now())
    update_user = Column(Integer)
    update_time = Column(DateTime, server_default=func.now())


class School(Base):
    """学校信息表."""

    __tablename__ = 'tf_school'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False)
    create_user = Column(Integer)
    create_date = Column(DateTime, server_default=func.now())
    update_user = Column(Integer)
    update_time = Column(DateTime, server_default=func.now())


class Courses(Base):
    """课程信息表."""

    __tablename__ = 'tf_courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False)
    create_user = Column(Integer)
    create_date = Column(DateTime, server_default=func.now())
    update_user = Column(Integer)
    update_time = Column(DateTime, server_default=func.now())


class TimeTable(Base):
    """课程表信息表."""

    __tablename__ = 'tf_timetable'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('tf_courses.id'))
    schedule = Column(String(32), nullable=False)
    content = Column(String(128), nullable=False)
    create_user = Column(Integer)
    create_date = Column(DateTime, server_default=func.now())
    update_user = Column(Integer)
    update_time = Column(DateTime, server_default=func.now())

    courses = relationship(
        'Courses',
        foreign_keys=[course_id],
        backref=backref('timetables')
    )


class Classes(Base):
    """班级信息表."""

    __tablename__ = 'tf_classes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False)
    course_id = Column(Integer, ForeignKey('tf_courses.id'))
    create_user = Column(Integer)
    create_date = Column(DateTime, server_default=func.now())
    update_user = Column(Integer)
    update_time = Column(DateTime, server_default=func.now())

    courses = relationship('Courses', foreign_keys=[
                           course_id], backref=backref('classes'))


# 创建所有定义好的表
Base.metadata.create_all(engine)
session = DBSession()
session.commit()
