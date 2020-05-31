# -*- coding:utf-8 -*-
"""
author: Luke
datettime: 2020/4/15 20:18
"""

"""
使用points更新数据， python ./plots/points.py
"""

import datetime
import json
import sys
import os
import argparse
from urllib import request

import pandas as pd
import requests
from dateutil.relativedelta import relativedelta
from sqlalchemy import NVARCHAR
from utils import engine, get_cut_val

sys.path.append(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])

from settings import username, password, authorization


def get_token():
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
        "authorization": authorization
    }

    url = "https://cloud.lk-cl.com:8443/oauth2/oauth/token?grant_type=password" \
          f"&scope=all&username={username}&password={password}"
    response = requests.post(url, headers=headers).text
    token = json.loads(response)['access_token']
    return token


def get_point(month):
    token = get_token()

    year = int(month[:4])
    month = int(month[5:])
    date = datetime.date(year, month, 1)

    start_date = datetime.date(date.year, date.month, 1)
    end_date = datetime.date(date.year, date.month, 1) + relativedelta(day=31)

    str_start_date = start_date.strftime('%Y-%m-%d')
    str_end_date = end_date.strftime('%Y-%m-%d')

    url = f"https://cloud.lk-cl.com:8443/mpmApi/integralReport/integralRange?access_token={token}" \
          f"&recordDate={str_start_date}&endDate={str_end_date}&accounts=all"

    response = request.urlopen(url)
    res = response.read().decode('utf-8')
    df = pd.DataFrame(json.loads(res)['data'])
    df['date'] = start_date.strftime('%Y%m')

    df = df[['bscoreMonth', 'userAccount', 'date']]
    df.columns = ['point', 'userAccount', 'date']

    return df


def get_classes(df):
    cut_v = get_cut_val(df)
    if not cut_v:
        df['score_class'] = None
        df['point_class'] = None
        return df

    df['score_class'] = pd.cut(df.score, cut_v, labels=list('ABCD'))
    df['point_class'] = pd.cut(df.point, cut_v, labels=list('ABCD'))
    return df


def prepare_cp_point(date):
    year = int(date[:4])
    month = int(date[5:])
    df_point = get_point(date)

    try:
        pd.read_sql(f"DELETE  FROM tmp_point  WHERE date = '{date}'", engine)
    except:
        pass
    # engine.execute(f"DELETE  FROM tmp_point  WHERE date = '{date}'")
    df_point.to_sql('tmp_point', engine, if_exists='append',
                    dtype={'userAccount': NVARCHAR('max'),'date': NVARCHAR('max')}
     )

    df_gb = pd.read_sql(f'''
    select
        lastname,
        total score_ori,
        point point_ori,
        cp_result.*,
        loginid,
           a_CpYgDepBind.supdepId,
        h1.departmentname supName,
           HrmResource.departmentid,
        h2.departmentname,
        rank() over (partition by years,months order by total desc) score,
        rank() over (partition by years,months order by total) score1,
        rank() over (partition by years,months order by point desc) point,
        rank() over (partition by years,months order by point) point1
    from cp_result
    INNER JOIN HrmResource  ON HrmResource.id = btprid
    INNER JOIN a_CpYgDepBind  ON a_CpYgDepBind.childId  = HrmResource.departmentid
    INNER JOIN HrmDepartment h1 ON h1.id = a_CpYgDepBind.supdepId
    INNER JOIN HrmDepartment h2 ON h2.id = HrmResource.departmentid
    INNER JOIN tmp_point on loginid = tmp_point.userAccount
    WHERE years = {year} AND months = {month}  and category = 6
    and tmp_point.date = {date}
    AND HrmResource.status in (0,1,2,3)
    ''', engine)
    df_gb = get_classes(df_gb)

    df_yg = pd.read_sql(f'''
    select
        lastname,
        total score_ori,
        point point_ori,
        cp_result.*,
        loginid,
           a_CpYgDepBind.supdepId,
        h1.departmentname supName,
           HrmResource.departmentid,
        h2.departmentname,
    rank() over (partition by years,months,a_CpYgDepBind.supdepId order by total desc) score,
    rank() over (partition by years,months,a_CpYgDepBind.supdepId order by total) score1,
    rank() over (partition by years,months,a_CpYgDepBind.supdepId order by point desc) point,
    rank() over (partition by years,months,a_CpYgDepBind.supdepId order by point) point1
    from cp_result
    INNER JOIN HrmResource  ON HrmResource.id = btprid
    INNER JOIN a_CpYgDepBind  ON a_CpYgDepBind.childId  = HrmResource.departmentid
    INNER JOIN HrmDepartment h1 ON h1.id = a_CpYgDepBind.supdepId
    INNER JOIN HrmDepartment h2 ON h2.id = HrmResource.departmentid
    INNER JOIN tmp_point on loginid = tmp_point.userAccount
    WHERE years = {year} AND months = {month}  and category = 7
    and tmp_point.date = {date}
    AND HrmResource.status in (0,1,2,3)
    ''', engine)
    df_yg = df_yg.groupby('supdepId').apply(get_classes)

    df = pd.concat([df_gb, df_yg], axis=0)

    try:
        pd.read_sql(f"DELETE  FROM result_all  WHERE date = '{date}'", engine)
    except:
        pass
    # engine.execute(f"DELETE  FROM result_all  WHERE date = '{date}'")
    df['date'] = date
    df.to_sql('result_all', engine, if_exists='append', index=False,
              dtype={'lastname': NVARCHAR('max'), 'supName': NVARCHAR('max'),
                     'departmentname': NVARCHAR('max'),'loginid': NVARCHAR('max'),
                     })  # todo 修改为append

    print(df.shape)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('month',type=str,help='月份，使用格式：202003')
    args = parser.parse_args()
    df = prepare_cp_point(args.month)
    print(f"Process data for {args.month} success.")
