#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2021/5/24 下午3:49
# @Author  : Hubert Shelley
# @Project  : Smart7_ORM
# @FileName: core.py
# @Software: PyCharm
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from smart7_orm import db
import settings


def make_sql():
    db_class = getattr(db, settings.database.pop('db'))
    return db_class(**settings.database)


def make_engine(sql: (db.SQLBase, db.SQLiteBase)):
    _engine = create_engine(sql.get_url(), echo=True, future=True)
    return _engine


Base = declarative_base()
engine = make_engine(make_sql())
Session = sessionmaker(bind=engine)
session = Session()
