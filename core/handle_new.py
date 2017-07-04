#! /usr/bin/env python
# -*-coding: utf-8 -*-
from hashlib import md5

from db import inittables
from db.inittables import session


class BaseUser(object):
    """基础用户类."""

    def __init__(self, ses=None):
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


class Tourist(BaseUser):
    """游客类.

    使用此系统未登录前所有人都是游客。
    """

    def _register(self, qq, name, sex, role_id)