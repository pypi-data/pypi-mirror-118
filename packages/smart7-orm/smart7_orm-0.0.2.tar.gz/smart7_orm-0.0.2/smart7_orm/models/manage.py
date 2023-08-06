#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2021/5/24 下午5:35
# @Author  : Hubert Shelley
# @Project  : Smart7_ORM
# @FileName: manage.py
# @Software: PyCharm
"""
import abc
from typing import Any

from sqlalchemy import exists, literal
from sqlalchemy.orm import Query

from smart7_orm.core import session as core_session


class ModelManageBase(metaclass=abc.ABCMeta):
    session = core_session

    def __init__(self, model=None, query_set: Query = None):
        self.model = model
        self.query_set: Query = query_set

    def get_queryset(self):
        if not self.query_set:
            self.query_set = self.session.query(self.model)
        return self.query_set

    @abc.abstractmethod
    def filter(self, **kwargs) -> 'ModelManageBase':
        pass

    @abc.abstractmethod
    def get(self, ident) -> Query:
        pass

    @abc.abstractmethod
    def first(self) -> Query:
        pass

    @abc.abstractmethod
    def all(self) -> Query:
        pass

    @abc.abstractmethod
    def sql_execute(self, sql: str) -> Query:
        pass

    @abc.abstractmethod
    def exists(self, **kwargs) -> bool:
        pass

    @abc.abstractmethod
    def delete(self) -> int:
        pass

    @abc.abstractmethod
    def update(self, values, synchronize_session="evaluate", update_args=None) -> int:
        pass


class ModelManage(ModelManageBase):
    def update(self, values, synchronize_session="evaluate", update_args=None) -> Any:
        return self.query_set.update(values, synchronize_session="evaluate", update_args=None)

    def delete(self, synchronize_session="evaluate") -> int:
        return self.query_set.delete(synchronize_session=synchronize_session)

    def exists(self, **kwargs) -> bool:
        query = self.filter(**kwargs)
        is_exists = self.session.query(literal(True)).filter(query.exists()).scalar()
        return is_exists

    def filter(self, **kwargs) -> 'ModelManage':
        if not self.query_set:
            self.get_queryset()
        return ModelManage(query_set=self.query_set.filter_by(**kwargs))

    def get(self, ident) -> Any:
        if not self.query_set:
            self.get_queryset()
        return self.query_set.get(ident)

    def first(self) -> Query:
        if not self.query_set:
            self.get_queryset()
        return self.query_set.first()

    def all(self) -> Query:
        if not self.query_set:
            self.get_queryset()
        return self.query_set.all()

    def sql_execute(self, sql: str) -> Query:
        pass


class ModelBase:
    session = core_session

    def save(self) -> Any:
        if self.__is_instance_exists():
            self.update()
            return self
        else:
            self.session.add(self)
            self.session.commit()
            return self

    def __get_changed_fields(self) -> dict:
        changed_dict = self.get_dict()
        changed_dict.pop('id')
        return changed_dict

    def __is_instance_exists(self):
        return self.objects.exists(id=self.id)

    def update(self) -> int:
        changed_dict = self.__get_changed_fields()
        if changed_dict:
            row_count = self.objects.update(changed_dict)
            return row_count
        return 0

    def delete(self):
        self.session.delete(self)
        self.session.commit()
