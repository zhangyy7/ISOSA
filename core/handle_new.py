#! /usr/bin/env python
# -*-coding: utf-8 -*-
import datetime
from hashlib import md5

from db import inittables
from db.inittables import session


class BaseUser(object):
    """基础用户类."""

    def __init__(self, ses=None):
        """实例化时绑定一个session到对象."""
        if session is None:
            self.session = session
        else:
            self.session = ses

    def _str2md5(self, value):
        """将字符串转成MD5值."""
        m = md5()
        m.update(value)
        md5_value = m.hexdigit()
        return md5_value

    def _add(self, obj):
        self.session.add(obj)
        self.session.commit()

    def _login(self, qq, password):
        pass


class Tourist(BaseUser):
    """游客类.

    使用此系统未登录前所有人都是游客。
    """

    def _register(self,
                  qq,
                  name,
                  sex,
                  role_id,
                  password=None,
                  register_date=datetime.datetime.now(),
                  update_user=1):

        if password is None:
            password = self._str2md5("123456")
        else:
            password = self._str2md5(password)
        user = inittables.UserInfo(
            qq=qq,
            name=name,
            sex=sex,
            role_id=role_id,
            password=password,
            register_date=register_date,
            update_user=update_user)
        self._add(user)
