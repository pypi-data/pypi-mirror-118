#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2021/5/24 下午3:57
# @Author  : Hubert Shelley
# @Project  : Smart7_ORM
# @FileName: SQLBase.py
# @Software: PyCharm
"""
import abc


class SQLBase(metaclass=abc.ABCMeta):
    def __init__(self, host: str = 'localhost', port: int = None, username: str = '', password: str = '',
                 db_name: str = 'default_database'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db_name = db_name

    @abc.abstractmethod
    def get_port(self) -> int:
        pass

    @abc.abstractmethod
    def get_name(self) -> str:
        pass

    def get_url(self) -> str:
        return f'{self.get_name()}://{self.username}:{self.password}@{self.host}:{self.get_port()}/{self.db_name}'


class SQLiteBase(metaclass=abc.ABCMeta):
    def __init__(self, path: str = 'sqlite.db',
                 db_name: str = 'default_database'):
        self.path = path
        self.db_name = db_name

    @abc.abstractmethod
    def get_name(self) -> str:
        pass

    def get_url(self) -> str:
        return f'{self.get_name()}:///{self.path}'
