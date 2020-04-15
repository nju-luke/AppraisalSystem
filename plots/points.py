# -*- coding:utf-8 -*-
"""
author: Luke
datettime: 2020/4/15 20:18
"""

from urllib import request
import json
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta


def get_point(month):
    year = int(month[:4])
    month = int(month[5:])
    date = datetime.date(year, month, 1)

    start_date = datetime.date(date.year, date.month, 1)
    end_date = datetime.date(date.year, date.month, 1) + relativedelta(day=31)

    str_start_date = start_date.strftime('%Y-%m-%d')
    str_end_date = end_date.strftime('%Y-%m-%d')

    url = f"https://cloud.lk-cl.com:8443/mpmApi/integralReport/integralRange?access_token=202a7519-ca6a-46b3-b1eb" \
          f"-46df3873d1b8&recordDate={str_start_date}&endDate={str_end_date}&accounts=all"

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
