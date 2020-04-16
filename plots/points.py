# -*- coding:utf-8 -*-
"""
author: Luke
datettime: 2020/4/15 20:18
"""

import datetime
import json
import sys
from urllib import request

import pandas as pd
import requests
from dateutil.relativedelta import relativedelta

sys.path.append("../..")

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
    df['date'] = month

    df = df[['bscoreMonth', 'userAccount', 'date']]
    df.columns = ['point', 'userAccount', 'date']

    return df


if __name__ == '__main__':
    month = '202003'
    df = get_point(month)
    print('done')
