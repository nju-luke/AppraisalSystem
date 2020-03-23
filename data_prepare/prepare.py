# -*- coding:utf-8 -*-
"""
author: byangg
datettime: 2020/3/23 14:47
"""

import datetime
import sys
import pandas as pd
from sqlalchemy import create_engine

from settings import *

engine = create_engine(f'mysql+pymysql://{user}:{pwd}@{host}:{port}/{database_name}')


def prepare_points(start_date, end_date):
    start_date = start_date[:7]
    engine.execute(f"delete from {target_points_table} where rec_month = '{start_date}'")
    sql = f'''insert into {target_points_table}
        select p.userAccount username,
               gp.scores     score,
               '{start_date}' rec_month
        from person p
                 join (
            select employeeid, sum(bscore * num) scores
            from integralevent
            where recordDate >= '{start_date}'
              and recordDate <= '{end_date}'
              and isDel = 0
            group by employeeid
        ) gp on trim(p.id) = trim(gp.employeeid)
        '''
    engine.execute(sql)
    print(f'prepare points for {start_date} success.')


def prepare_appraise(start_date, end_date):
    start_date = start_date[:7]         ## 将开始日期的月份作为当前数据的日期存储
    engine.execute(f"delete from {target_appraise_dtl_table} where txrq = '{start_date}'")
    dtl_sql = f'''
        insert into {target_appraise_dtl_table}
        select '{start_date}' txrq, txr, t5.loginid txr_loginid,t5.lastname txr_name,
               f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,
               f1+f2+f3+f4+f5+f6+f7+f8+f9+f10+f11 score,
               bsbtpr, t4.loginid bs_loginid, t4.lastname bs_name
        from formtable_main_114 t1
        INNER JOIN workflow_currentoperator t3 ON t3.requestid = t1.requestId
        INNER JOIN HrmResource t5 ON t5.id = t1.txr
        INNER JOIN formtable_main_114_dt1 t2 ON t2.mainid = t1.id
        INNER JOIN HrmResource t4 ON t4.id = t2.bsbtpr
        WHERE (t3.isremark = 4) AND (t3.iscomplete = 1)
          AND txr <> bsbtpr
          -- 去除重複
          AND t2.id not in (
            select MAX(t2.id) as id
            FROM formtable_main_114 t1
                     INNER JOIN formtable_main_114_dt1 t2 ON t2.mainid = t1.id
                     INNER JOIN workflow_currentoperator t4 ON t4.requestid = t1.requestId
            WHERE (t4.isremark = 4) AND (t4.iscomplete = 1)
            and txrq >= '{start_date}' and txrq <= '{end_date}'
            GROUP BY txr, bsbtpr
            HAVING COUNT(*) > 1
        )
        and txrq >= '{start_date}' and txrq <= '{end_date}'
    '''
    engine.execute(dtl_sql)

    engine.execute(f"delete from {target_appraise_table} where txrq = '{start_date}'")
    sql = f'''
        insert into {target_appraise_table} 
        select txrq, dtl.txr_loginid, txr_name,
               case when std1 <> 0 then
                   (score - av1 ) / std1 * 5 + 80
                else 80 end score_w,
               bs_loginid, bs_name
        from report_appraise_dtl dtl
        join(
            select txr_loginid, avg(score) av1, std(score) std1
            from report_appraise_dtl
            where txrq = '{start_date}'
            group by txr_loginid
        ) sta on dtl.txr_loginid = sta.txr_loginid
        where txrq = '{start_date}'
    '''
    engine.execute(sql)

    print('prepare appraise for {start_date} success.')


def prepare_auth():
    df = pd.read_sql('select id, loginid, managerid from hrmresource', engine)
    auths = {0: '0', 412: '0'}

    while True:
        _dic = {}
        for id, loginid, managerid in df.values:
            if id in auths or managerid not in auths: continue
            _dic[managerid] = _dic.setdefault(managerid, 0) + 1
            auths[id] = auths[managerid] + '%02d' %_dic[managerid]
        if len(_dic) == 0:
            break
    print(auths)





def main(start_date, end_date):
    # prepare_points(start_date, end_date)
    # prepare_appraise(start_date, end_date)
    # prepare_all(start_date, end_date)

    prepare_auth()


if __name__ == '__main__':
    if len(sys.argv) > 2:
        start_date = sys.argv[1]
        end_date = sys.argv[2]
    elif len(sys.argv) == 2:
        start_date = sys.argv[1]
        end_date = datetime.date.today().strftime('%Y-%m-%d')
    else:
        start_date = datetime.date.today().strftime('%Y-%m')
        end_date = datetime.date.today().strftime('%Y-%m-%d')

    main(start_date, end_date)
    print(f"{start_date} ~ {end_date} 的数据处理完成！")
