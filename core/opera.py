#! /usr/bin/env python
# -*- coding:utf-8 -*-
from db.inittables import session
from db import inittables

user1 = inittables.User(
    qq=910709054,
    name='张寅月',
    sex='M',
    update_user=910709054
)

session.add(user1)
session.commit()
