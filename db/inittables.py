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


class SchoolInfo(Base):
    """学校信息表."""

    __tablename__ = 'tf_school'
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), unique=True, nullable=False)
    location = Column("location", String(128))
    headmaster_id = Column("headmaster_id", Integer, ForeignKey("tf_user.id"))
    update_time = Column(DateTime, server_default=func.now())

    # 添加关系属性（关联到headmater_id外键上）
    headmaster = relationship("UserInfo", foreign_keys=[headmaster_id])


class UserInfo(Base):
    """用户信息类."""

    __tablename__ = 'tf_user'
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    qq = Column("qq", Integer, unique=True)
    name = Column("name", String(32), nullable=False)
    sex = Column("sex", Enum('M', 'F'), server_default='M')
    age = Column("age", Integer, nullable=False)
    role_id = Column("role_id", Integer, ForeignKey("tf_role.id"))
    password = Column(
        "password",
        String(128),
        nullable=False,
        server_default=func.md5("123456"))
    status = Column("status", String(1), server_default='1')
    register_date = Column(
        "register_date", DateTime, server_default=func.now())
    update_time = Column("update_time", DateTime, server_default=func.now())
    update_user = Column("update_user_id", Integer, ForeignKey("tf_user.id"))

    # 添加关系属性（关联到role_id外键上）
    roles = relationship(
        'RoleInfo', foreign_keys=[role_id], backref=backref("users"))


class RoleInfo(Base):
    """角色信息表映射类."""

    __tablename__ = 'tf_role'
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), unique=True, nullable=False)


class Courses(Base):
    """课程信息表."""

    __tablename__ = 'tf_courses'
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(128), unique=True, nullable=False)
    price = Column("price", Integer, nullable=False)
    cycle = Column("cycle", Integer)
    update_user_id = Column("update_user_id", Integer,
                            ForeignKey("tf_user.id"))
    update_time = Column("update_time", DateTime, server_default=func.now())


class Classes(Base):
    """班级信息表."""

    __tablename__ = 'tf_classes'
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

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
    students = relationship(
        'ClassesStudentRef', foreign_keys="tr_classes_student_ref.students")


class ClassesStudentRef(Base):
    """班级与学员关系表."""

    __tablename__ = "tr_classes_student_ref"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    classes_id = Column("classes_id", Integer, ForeignKey("tf_classes.id"))
    student_id = Column("student_id", Integer, ForeignKey("tf_user.id"))
    opera_teacher_id = Column("opera_teacher_id", Integer,
                              ForeignKey("tf_user.id"))
    update_time = Column("update_time", DateTime, server_default=func.now())

    classes = relationship('Classes', foreign_keys=[classes_id])
    students = relationship('UserInfo', foreign_keys=[student_id])


class CourseModular(Base):
    """课程模块表."""

    __tablename__ = 'tf_curriculum_schedule'
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(128))
    course_id = Column("course_id", Integer, ForeignKey("tf_courses.id"))
    update_teacher_id = Column(Integer, ForeignKey("tf_user.id"))
    update_time = Column(DateTime, server_default=func.now())


class CurriculumSchedule(Base):
    """课程安排表."""

    __tablename__ = 'tf_curriculum_schedule'
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8"}

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    course_id = Column("course_id", Integer, ForeignKey("tf_courses.id"))
    modular_id = Column(Integer, ForeignKey("tf_curriculum_shedule.id"))
    content_summary = Column(String(128))
    sequence_number = Column(Integer)
    time_consuming = Column(Integer)
    update_teacher_id = Column(Integer, ForeignKey("tf_user.id"))
    update_time = Column(DateTime, server_default=func.now())


# 创建所有定义好的表
Base.metadata.create_all(engine)
