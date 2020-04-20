# -*- coding:utf-8 -*-
"""
author: byangg
datettime: 2020/4/18 17:07
"""
from sqlalchemy import create_engine
import sys
import os

sys.path.append(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])

from settings import MSSQL_SETTINGS

USER = MSSQL_SETTINGS.USER
PASSWORD = MSSQL_SETTINGS.PASSWORD
HOST = MSSQL_SETTINGS.HOST
DATABASE = MSSQL_SETTINGS.NAME
DRIVER = MSSQL_SETTINGS.DRIVER.replace(' ', '+')


def sql_engine():
    engine_str = "mssql+pyodbc://" + USER + ":" + PASSWORD + "@" + HOST + "/" + DATABASE + "?driver=" + DRIVER
    engine = create_engine(engine_str)
    return engine


engine = sql_engine()


def get_cut_val(df):
    num_emp = len(df)
    if num_emp < 4:
        return None
    n_ab = int(num_emp * 0.3)
    n_ab = n_ab if n_ab > 1 else 1
    n_d = int(num_emp * 0.1)
    n_d = n_d if n_d > 1 else 1
    n_c = num_emp - n_d
    cut_v = [0, n_ab, n_ab * 2, n_c, num_emp + 0.01]
    return cut_v