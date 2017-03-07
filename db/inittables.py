#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""连接数据库，初始化表."""
import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from conf import settings


# 初始化数据库连接
engine = create_engine(settings.database[settings.engine])

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
    update_user = Column(Integer)
    update_time = Column(DateTime, default=datetime.datetime.now())


Base.metadata.create_all(engine)

session = DBSession()

user1 = User(
    qq=910709054,
    name='zhangyy',
    age=30,
    update_user=910709054,
)

session.add(user1)
session.commit()
