#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2021/5/24 下午5:35
# @Author  : Hubert Shelley
# @Project  : Smart7_ORM
# @FileName: models.py
# @Software: PyCharm
"""
import inspect

from smart7_orm.core import Base
from .fields import IntegerField
from .manage import ModelManage, ModelBase


def _has_contribute_to_class(value):
    # Only call contribute_to_class() if it's bound.
    return not inspect.isclass(value) and hasattr(value, 'contribute_to_class')


class Model(Base, ModelBase):
    # 定义抽象类
    __abstract__ = True

    id = IntegerField(primary_key=True, autoincrement=True)

    # objects: ModelManage = Model.set_manage_class()
    objects: ModelManage = None

    def get_dict(self):
        return dict((column.name, getattr(self, column.name))
                    for column in self.__table__.columns)

    @classmethod
    def manage_ready(cls):
        cls.objects = ModelManage(cls)
