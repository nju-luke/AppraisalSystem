# -*- coding:utf-8 -*-
"""
author: Luke
datettime: 2020/4/15 20:59
"""

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AppraisalSystem.settings")  # project_name 项目名称
django.setup()

from django.contrib.auth.hashers import make_password, check_password
from settings import MSSQL_SETTINGS
from sqlalchemy import create_engine
import pandas as pd
import sys

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


print(sys.argv)
data_path = sys.argv[1]
df = pd.read_csv(data_path, sep='\t')
# df = pd.read_csv('Django_assets/test_usr_pwd.tsv', sep='\t')

df['is_superuser'] = 0
df['is_staff'] = 1
df[ 'is_active'] = 1
df['first_name'] = ''
df['last_name'] = ''
df['email'] = ''
df['date_joined'] = ''
df['password'] = df['password'].apply(make_password)

df.to_sql('auth_user', engine, if_exists='append', index=False)

print(f'create user from {sys.argv[1]} success.'
      'the user has been create to table auth_user'
      )



# password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined

