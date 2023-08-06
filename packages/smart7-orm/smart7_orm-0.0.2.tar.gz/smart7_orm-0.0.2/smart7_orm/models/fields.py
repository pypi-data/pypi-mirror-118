#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2021/5/24 下午5:35
# @Author  : Hubert Shelley
# @Project  : Smart7_ORM
# @FileName: fields.py
# @Software: PyCharm
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, SmallInteger, DateTime, ForeignKey, Time, JSON


def IntegerField(**kwargs):
    return Column(Integer, **kwargs)


def StringField(max_length, **kwargs):
    return Column(String(max_length), **kwargs)


def TextField(**kwargs):
    return Column(Text, **kwargs)


def JsonField(**kwargs):
    return Column(JSON, **kwargs)


def BooleanField(**kwargs):
    return Column(Boolean, **kwargs)


def SmallIntegerField(**kwargs):
    return Column(SmallInteger, **kwargs)


def DateTimeField(**kwargs):
    return Column(DateTime, **kwargs)


def TimeField(**kwargs):
    return Column(Time, **kwargs)


def ForeignKeyField(model, fk_field: str = 'id', field_type=Integer, **kwargs):
    return Column(field_type, ForeignKey(f'{model.__tablename__}.{fk_field}'), **kwargs)
