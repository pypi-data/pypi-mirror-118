#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2021/5/27 下午1:56
# @Author  : Hubert Shelley
# @Project  : Smart7_ORM
# @FileName: setup.py
# @Software: PyCharm
"""
from smart7_orm.core import engine
from smart7_orm.models import Model
from smart7_orm.logger import logger


def auto_instance(_model=Model):
    if _model is Model:
        logger.info("model ready start")
    for sub_class in _model.__subclasses__():
        if hasattr(sub_class, '__tablename__'):
            sub_class.manage_ready()
            sub_class.metadata.create_all(engine)
            logger.info(f"{sub_class.__name__} is ready")
        if len(sub_class.__subclasses__()) > 0:
            auto_instance(sub_class)
    if _model is Model:
        logger.info("all model is ready")


print("""
                ooooooooooooooooooooooooooooooooooooooooooooooooooooo
                ooooooooooooooooooooooooooooooooooooooooooooooooooooo
                ooooooooooooooooooooooooooooooooooooooooooooooooooooo
                ooooo^************************,]]]oooooooo[ ,/ooooooo
                ooooo^****************,]oooooooooooooo[***/oooooooooo
                ooooo^**********,/ooooooooooooooooo/ ***,oooooooooooo
                ooooo^******,/ooooooooooooooooooo/*****=ooooooooooooo
                ooooo^***,oooooooooooooooooooooo`*****=oooooooooooooo
                ooooo^*,oooooooooooooooooooooo/******=ooooooooooooooo
                ooooo^/oooooooooooooooooooooo^******,oooooooooooooooo
                oooooooooooooooooooooooooooo`*******ooooooooooooooooo
                ooooooooooooooooooooooooooo`*******=ooooooooooooooooo
                oooooooooooooooooooooooooo^********oooooooooooooooooo
                ooooooooooooooooooooooooo^********=oooooooooooooooooo
                ooooooooooooooooooooooooo*********ooooooooooooooooooo
                oooooooooooooooooooooooo^********=ooooooooooooooooooo
                ooooooooooooooooooooooo/*********=ooooooooooooooooooo
                ooooooooooooooooooooooo^*********oooooooooooooooooooo
                ooooooooooooooooooooooo*********,oooooooooooooooooooo
                oooooooooooooooooooooo^*********=oooooooooooooooooooo
                oooooooooooooooooooooo^*********=oooooooooooooooooooo
                oooooooooooooooooooooo**********=oooooooooooooooooooo
                oooooooooooooooooooooo**********ooooooooooooooooooooo
                oooooooooooooooooooooo**********ooooooooooooooooooooo
                oooooooooooooooooooooo]]]]]]]]]]ooooooooooooooooooooo
                ooooooooooooooooooooooooooooooooooooooooooooooooooooo
                ooooooooooooooooooooooooooooooooooooooooooooooooooooo
""")
print('Smart7 ORM running')
auto_instance()
