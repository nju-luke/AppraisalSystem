# -*- coding:utf-8 -*-
"""
author: byangg
datettime: 2020/5/15 9:49
"""

# -*- coding:utf-8 -*-
"""
author: byangg
datettime: 2020/3/20 14:00
"""
import json
import string
import datetime
from copy import deepcopy

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from _plotly_utils.utils import PlotlyJSONEncoder
from dateutil.relativedelta import relativedelta
from django.urls import reverse

from .utils import engine, get_cut_val

import os

os.environ['DJANGO_SETTINGS_MODULE'] = "AppraisalSystem.settings"

TABLE_COLS = ['lastname', 'score_ori', 'score', 'score_class',
              'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11',
              'point_ori', 'point', 'point_class']
TABLE_COLS_EMP = ['lastname', 'score_ori', 'score', 'score_class',
                  'v1', 'v2', 'v3', 'v4', 'v5',
                  'point_ori', 'point', 'point_class']
SHOW_COLS = {'lastname': '姓名', 'score_ori': '测评分', 'score': '测评排名', 'score_class': '测评等级',
             'v1': '客户意识(15)', 'v2': '成本意识(10)', 'v3': '责任心(10)', 'v4': '日清日毕(10)', 'v5': '坚持力(10)',
             'v6': '领导力(10)', 'v7': '学习创新(10)', 'v8': '团队协作(10)', 'v9': '公平公正(5)', 'v10': '廉洁诚信(5)', 'v11': '微笑服务(5)',
             'point_ori': '积分', 'point': '积分排名', 'point_class': '积分等级',
             'txrName': '测评人', 'total': '总分'
             }

SHOW_COLS_EMP = {'lastname': '姓名', 'score_ori': '测评分', 'score': '测评排名', 'score_class': '测评等级',
                 'v1': '责任心(满分30)', 'v2': '执行力(满分20)', 'v3': '团队协作(满分20)', 'v4': '工作不推诿(满分20)', 'v5': '日清日毕(满分10)',
                 'point_ori': '积分', 'point': '积分排名', 'point_class': '积分等级',
                 'txrName': '测评人', 'total': '总分'
                 }

PERM_COLS = ['txrName', 'total', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11']
PERM_COLS_EMP = ['txrName', 'total', 'v1', 'v2', 'v3', 'v4', 'v5']


def get_areas():
    df_area = pd.DataFrame([[1, 1, 2, 2, 1], [1, 2, 2, 1, 1]]).T * 10

    df_area1 = df_area.copy()

    df_area[0] += 40
    df_area[1] += 40

    df_area1[0] += 70
    df_area1[1] += 70

    return df_area, df_area1


def stuff_plot(username):
    # username = 'name1'
    # sql = f"select * from test_data where username='{username}'"
    #
    # df = pd.read_sql(sql, engine)
    # areas = get_areas()

    nums = 20
    df = pd.DataFrame(np.random.randn(nums, 2) * 10 + 70, dtype=np.int,
                      columns=['x', 'y'], index=list(range(nums)))

    df['name'] = [f'员工_{string.ascii_uppercase[i]}' for i in range(nums)]
    df = df.groupby(['x', 'y'])['name'].agg(
        lambda x: ','.join(x)).reset_index()

    df_area = pd.DataFrame([[1, 1, 2, 2, 1], [1, 2, 2, 1, 1]]).T * 10

    df_area1 = df_area.copy()

    df_area[0] += 40
    df_area[1] += 40

    df_area1[0] += 70
    df_area1[1] += 70

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df_area[0], y=df_area[1], line_color='Coral',
                   mode='lines', fill='toself', fillcolor='LightSalmon',
                   name='Warn'))
    fig.add_trace(
        go.Scatter(x=df_area1[0], y=df_area1[1], line_color='lightskyblue',
                   mode='lines', fill='toself', name='Pef'))
    fig.add_trace(go.Scatter(x=df['x'], y=df['y'], text=df['name'],
                             mode='markers + text', textposition='top center'))

    fig.update_layout(showlegend=False, height=800, )

    # fig.show()

    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)

    return graphJSON

    # plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    # return plot_div


def get_area(df):
    # xs = np.quantile(df.score.astype(float), [0, 0.25, 0.5, 0.75, 1])
    # ys = np.quantile(df.point.astype(float), [0, 0.25, 0.5, 0.75, 1])
    xs = get_cut_val(df)
    if not xs: return None

    xs = [max(xs) - v for v in xs]
    ys = xs

    # xs[0] -= 5
    # xs[-1] += 5
    # ys[0] -= 5
    # ys[-1] += 5

    area1_x = [xs[0], xs[1], xs[1], xs[0], xs[0]]
    area1_y = [ys[0], ys[0], ys[1], ys[1], ys[0]]

    area2_x = [xs[4], xs[2], xs[2], xs[1], xs[1], xs[0], xs[0], xs[1], xs[1], xs[4], xs[4]]
    area2_y = [ys[1], ys[1], ys[2], ys[2], ys[4], ys[4], ys[1], ys[1], ys[0], ys[0], xs[1]]

    area3_x = [xs[4], xs[3], xs[3], xs[1], xs[1], xs[2], xs[2], xs[4], xs[4]]
    area3_y = [ys[3], ys[3], ys[4], ys[4], ys[2], ys[2], ys[1], ys[1], ys[3]]

    area4_x = [xs[3], xs[4], xs[4], xs[3], xs[3]]
    area4_y = [ys[3], ys[3], ys[4], ys[4], ys[3]]

    return area1_x, area1_y, \
           area2_x, area2_y, \
           area3_x, area3_y, \
           area4_x, area4_y


# def get_data(month, category):
#     year = int(month[:4])
#     month = int(month[5:])
#     sql = f'''
#         select loginid,
#                lastname,
#                total score, point,
#                v1 ,v2 ,v3 ,v4 ,v5 ,v6 ,v7 ,v8 ,v9 ,v10,v11,
#                departmentid,
#                row_number() over (order by total desc) num
#         from cp_result where years={year} and months={month}
#         and category={category}
#             '''
#     df = pd.read_sql(sql, engine)
#     area1_x, area1_y, area2_x, area2_y = get_area(df)
#     return df, area1_x, area1_y, area2_x, area2_y

def get_data(date, category, depart=None):
    year = int(date[:4])
    month = int(date[5:])

    # sql = f'''
    #     select
    #         lastname,
    #         total score_ori,
    #         point point_ori,
    #         cp_result.*,
    #         loginid,
    #         HrmDepartment.departmentname, HrmResource.departmentid,
    #         rank() over (partition by years,months order by total desc) score,
    #         rank() over (partition by years,months order by total) score1,
    #         rank() over (partition by years,months order by point desc) point,
    #         rank() over (partition by years,months order by point) point1
    #     from cp_result
    #     INNER JOIN HrmResource  ON HrmResource.id = btprid
    #     INNER JOIN a_CpYgDepBind  ON a_CpYgDepBind.childId  = HrmResource.departmentid
    #     INNER JOIN HrmDepartment ON HrmDepartment.id = a_CpYgDepBind.supdepId
    #     INNER JOIN tmp_point on loginid = tmp_point.userAccount
    #     WHERE years = {year} AND months = {month}  and category = {category}
    #     AND HrmResource.status in (0,1,2,3)
    # '''

    sql = f'''
        select * from result_all
        where years = {year} AND months = {month}  and category = {category}
    '''

    if category == 6:
        pass
    elif category == 7:
        assert depart is not None
        sql += f" and supdepId = {depart}"
    else:
        raise ValueError(f"Cant find the category of {category}")

    sql += " order by score_ori desc"

    print(sql)
    # df_ap = pd.read_sql(sql, engine)
    # df_point = get_point(date)  # todo 使用字典保存每个月的数据
    # df = pd.merge(df_ap, df_point, left_on='loginid', right_on='userAccount')
    df = pd.read_sql(sql, engine)
    df['hover_txt'] = '测评：' + df.score.astype(str) + f'/{len(df)}' + ",积分：" + + df.point.astype(str) + f'/{len(df)}'
    # area1_x, area1_y, area2_x, area2_y = get_area(df)
    areas = get_area(df)
    return df, areas


def get_base_chart(month, group, depart=None):
    df, areas = get_data(month, group, depart)
    df['url'] = "<a target='_parent'  href='/appraisal/dtl?name=" + df.loginid + f"&month={month}" \
                + f"&group={group}" + f"&depart={depart}" + "'>" + df.lastname + "</a>"
    # df['url'] = "<a href='" + reverse("dtl") + "?name=" + df.loginid + f"&month={month}" \
    #             + f"&group={group}" + f"&depart={depart}" + "'>" + df.lastname + "</a>"
    point = go.Scatter(x=df.score1, y=df.point1, mode='markers + text', marker=dict(color='blue'),
                       text=df.url, textposition='top center',
                       hovertext=df['hover_txt'],
                       hoverinfo='text'
                       )
    if areas:
        # https://www.color-hex.com/color/7fffd4
        str_colors = "#349bff #66d8ff #7fdfff #99e5ff"
        colors = str_colors.split(" ")
        area1_x, area1_y, area2_x, area2_y, area3_x, area3_y, area4_x, area4_y = areas
        area1 = go.Scatter(x=area1_x, y=area1_y, line_color=colors[3], fillcolor=colors[3],
                           mode='lines', fill='toself', name='Perfect')
        area2 = go.Scatter(x=area2_x, y=area2_y, line_color=colors[2], fillcolor=colors[2],
                           mode='lines', fill='toself', name='Medium')
        area3 = go.Scatter(x=area3_x, y=area3_y, line_color=colors[1], fillcolor=colors[1],
                           mode='lines', fill='toself', name='Normal')
        area4 = go.Scatter(x=area4_x, y=area4_y, line_color=colors[0], fillcolor=colors[0],
                           mode='lines', fill='toself', name='Pool')

        fig = go.Figure([area1, area2, area3, area4, point])
    else:
        fig = go.Figure([point])
    fig.update_layout(xaxis={
        'title': '测评'},
        yaxis={'title': '积分'},
        autosize=False,
        width=980,
        height=800,
        showlegend=False)
    return df, fig


def get_loginid_id():
    df = pd.read_sql('''
    select loginid, id from HrmResource
    ''', engine)

    loginid_id = {l: i for l, i in df.values}
    return loginid_id


def get_html(df):
    # html = df.to_html(index=False, classes='table-striped', border=0).replace(
    #    'dataframe', 'table').replace('<tr>', '<tr style=" white-space:nowrap" class="text-center">'). \
    #    replace('<tr style="text-align: right;">', '<tr style=" white-space:nowrap" class="text-center">')

    html = df.to_html(index=False, classes='table-striped', border=0).replace(
        'dataframe', 'table').replace('<tr>', '<tr style=" white-space:nowrap" class="text-center">'). \
        replace('<tr style="text-align: right;">', '<tr style=" white-space:nowrap" class="text-center">')

    return html


class ChartsGallery():
    charts = {}
    dataframes = {}

    charts_emp = {}
    dataframes_emp = {}

    loginid_id = get_loginid_id()

    def initialize_chart(self, month, group):
        df, chart = get_base_chart(month, group)
        self.charts[(month, group)] = chart
        self.dataframes[(month, group)] = df

    def initialize_chart_emp(self, month, group, depart):
        df, chart = get_base_chart(month, group, depart)
        self.charts_emp[(month, group, depart)] = chart
        self.dataframes_emp[(month, group, depart)] = df

    def _get_department_auth(self, username):
        # todo 权限
        pass

    def get_chart_gb(self, name, month, department=None, group=None):
        if not (month, group) in self.charts:
            self.initialize_chart(month, group)
        chart = deepcopy(self.charts[(month, group)])  # 需要做copy

        if not department:
            indices = list(self.dataframes[(month, group)].loginid == name)
        else:
            indices = list(self.dataframes[(month, group)].departmentid.isin(department))

        text = [self.dataframes[(month, group)].url[i] if v else None for i, v in enumerate(indices)]
        hover_txt = [self.dataframes[(month, group)].hover_txt[i] if v else None for i, v in enumerate(indices)]
        chart.data[-1].update({'text': text, 'hovertext': hover_txt})
        graphJason = json.dumps(chart, cls=PlotlyJSONEncoder)
        return graphJason, self.dataframes[(month, group)][indices]

    def get_chart_emp(self, name, month, department=None, group=None, depart=None):
        if not (month, group, depart) in self.charts_emp:
            self.initialize_chart_emp(month, group, depart)

        chart = deepcopy(self.charts_emp[(month, group, depart)])  # 需要做copy

        if not department:
            indices = list(self.dataframes_emp[(month, group, depart)].loginid == name)
        else:
            indices = list(self.dataframes_emp[(month, group, depart)].departmentid.isin(department))

        text = [self.dataframes_emp[(month, group, depart)].url[i] if v else None for i, v in enumerate(indices)]
        hover_txt = [self.dataframes_emp[(month, group, depart)].hover_txt[i] if v else None for i, v in
                     enumerate(indices)]
        chart.data[-1].update({'text': text, 'hovertext': hover_txt})
        graphJason = json.dumps(chart, cls=PlotlyJSONEncoder)
        return graphJason, self.dataframes_emp[(month, group, depart)][indices]

    def get_chart(self, name, month, department=None, group=None, sup_depart=None):
        if group == 6:
            graph, df = self.get_chart_gb(name, month, department, group)

            table = df[TABLE_COLS]
            table = get_html(table.rename(columns=SHOW_COLS))
            return graph, table
        if group == 7:
            graph, df = self.get_chart_emp(name, month, department, group, depart=sup_depart)
            table = df[TABLE_COLS_EMP]
            table = get_html(table.rename(columns=SHOW_COLS_EMP))
            return graph, table

        raise ValueError

    def get_chart_and_dtl(self, name, month, group=7, sup_depart=None, is_sup_perm=False, isDetails=False):
        graph, table = self.get_chart(name, month, group=group, sup_depart=sup_depart)
        if is_sup_perm:
            cp_dtl = self.get_dtl_table(name, month, group, isDetails)
        else:
            cp_dtl = None

        return graph, table, cp_dtl

    def get_dtl_table(self, name, month, group, isDetails=False):
        id = self.loginid_id[name]
        cur_date = datetime.date(int(month[:4]), int(month[5:]), 1)

        start_date = cur_date + relativedelta(day=31) + datetime.timedelta(days=1)
        end_date = start_date + relativedelta(day=31) + datetime.timedelta(days=1)

        if isDetails:
            dtails = "t5.lastname as txrName"
        else:
            dtails = "'******' as txrName"

        if group == 7:
            sql = f'''
            -- 员工
            SELECT  -- t1.txr,
               {dtails},
               -- t2.bsbtpr,
               -- t4.lastname as btprName,
               -- t4.loginid,
                   (convert(Int, s1.name) + convert(Int, s2.name) + convert(Int, s3.name)
                       + convert(Int, s4.name) + convert(Int, s5.name))
                               as total,
                   s1.name     as v1,
                   s2.name     as v2,
                   s3.name     as v3,
                   s4.name     as v4,
                   s5.name     as v5
            FROM formtable_main_130 t1
                     INNER JOIN formtable_main_130_dt1 t2 ON t2.mainid = t1.id

                     INNER JOIN workflow_currentoperator t3 ON t3.requestid = t1.requestId
                     INNER JOIN HrmResource t4 ON t4.id = t2.bsbtpr
                     INNER JOIN HrmResource t5 ON t5.id = t1.txr

                     INNER JOIN a_CpYgDepBind t6 ON t6.childId = t4.departmentid
                     INNER JOIN a_CpYgDepBind t7 ON t7.childId = t5.departmentid

                     INNER JOIN mode_selectitempagedetail s1 ON s1.mainid = 22 AND s1.disorder = t2.f1
                     INNER JOIN mode_selectitempagedetail s2 ON s2.mainid = 23 AND s2.disorder = t2.f2
                     INNER JOIN mode_selectitempagedetail s3 ON s3.mainid = 23 AND s3.disorder = t2.f3
                     INNER JOIN mode_selectitempagedetail s4 ON s4.mainid = 23 AND s4.disorder = t2.f4
                     INNER JOIN mode_selectitempagedetail s5 ON s5.mainid = 23 AND s5.disorder = t2.f5
            WHERE
            --被打分人
                t2.bsbtpr = {id}
              AND t1.txrq >= '{start_date}'
              AND t1.txrq < '{end_date}'
              AND t6.supdepId = t7.supdepId

              AND (t3.isremark = 4)
              AND (t3.iscomplete = 1)

              AND t1.txr <> t2.bsbtpr
              -- 去重复
              AND t2.id not in (
                select MAX(t2.id) as id
                FROM formtable_main_114 t1
                         INNER JOIN formtable_main_114_dt1 t2 ON t2.mainid = t1.id
                         INNER JOIN workflow_currentoperator t4 ON t4.requestid = t1.requestId
                WHERE (t4.isremark = 4)
                  AND (t4.iscomplete = 1)
                  --被打分人
                  AND bsbtpr = {id}
                  AND t1.txrq >= '{start_date}'
                  AND t1.txrq < '{end_date}'
                GROUP BY txr, bsbtpr
                HAVING COUNT(*) > 1)
            '''
        elif group == 6:
            sql = f'''
            SELECT -- t1.txr,
                {dtails},
               -- t2.bsbtpr,
               -- t4.lastname as btprName,
               -- t4.loginid,
               (convert(Int, s1.name) + convert(Int, s2.name) + convert(Int, s3.name)
                   + convert(Int, s4.name) + convert(Int, s5.name) + convert(Int, s6.name) + convert(Int, s7.name)
                   + convert(Int, s8.name) + convert(Int, s9.name) + convert(Int, s10.name) + convert(Int, s11.name))
                           as total,
               s1.name     as v1,
               s2.name     as v2,
               s3.name     as v3,
               s4.name     as v4,
               s5.name     as v5,
               s6.name     as v6,
               s7.name     as v7,
               s8.name     as v8,
               s9.name     as v9,
               s10.name    as v10,
               s11.name    as v11
        FROM formtable_main_114 t1
                 INNER JOIN formtable_main_114_dt1 t2 ON t2.mainid = t1.id
                 INNER JOIN workflow_currentoperator t3 ON t3.requestid = t1.requestId
                 INNER JOIN HrmResource t4 ON t4.id = t2.bsbtpr

                 INNER JOIN HrmResource t5 ON t5.id = t1.txr

                 INNER JOIN mode_selectitempagedetail s1 ON s1.mainid = 24 AND s1.disorder = t2.f1
                 INNER JOIN mode_selectitempagedetail s2 ON s2.mainid = 13 AND s2.disorder = t2.f2
                 INNER JOIN mode_selectitempagedetail s3 ON s3.mainid = 13 AND s3.disorder = t2.f3
                 INNER JOIN mode_selectitempagedetail s4 ON s4.mainid = 13 AND s4.disorder = t2.f4
                 INNER JOIN mode_selectitempagedetail s5 ON s5.mainid = 13 AND s5.disorder = t2.f5
                 INNER JOIN mode_selectitempagedetail s6 ON s6.mainid = 13 AND s6.disorder = t2.f6
                 INNER JOIN mode_selectitempagedetail s7 ON s7.mainid = 13 AND s7.disorder = t2.f7
                 INNER JOIN mode_selectitempagedetail s8 ON s8.mainid = 13 AND s8.disorder = t2.f8
                 INNER JOIN mode_selectitempagedetail s9 ON s9.mainid = 21 AND s9.disorder = t2.f9
                 INNER JOIN mode_selectitempagedetail s10 ON s10.mainid = 21 AND s10.disorder = t2.f10
                 INNER JOIN mode_selectitempagedetail s11 ON s11.mainid = 21 AND s11.disorder = t2.f11
        WHERE (t3.isremark = 4)
          AND (t3.iscomplete = 1)
          --被打分人
          AND  t2.bsbtpr = {id}
          AND t1.txrq >= '{start_date}'
          AND t1.txrq < '{end_date}'
          -- 去重复
          AND t2.id not in (
            select MAX(t2.id) as id
            FROM formtable_main_114 t1
                     INNER JOIN formtable_main_114_dt1 t2 ON t2.mainid = t1.id
                     INNER JOIN workflow_currentoperator t4 ON t4.requestid = t1.requestId
            WHERE (t4.isremark = 4)
              AND (t4.iscomplete = 1)
              --被打分人
              AND  t2.bsbtpr = {id}
              AND t1.txrq >= '{start_date}'
              AND t1.txrq < '{end_date}'
            GROUP BY txr, bsbtpr
            HAVING COUNT(*) > 1
        )
          AND t4.id <> t5.id
            '''
        else:
            raise ValueError(group)
        df = pd.read_sql(sql, engine)

        # table = table.rename(columns=SHOW_COLS).to_html(index=False, classes='table-striped', border=0).replace(
        #     'dataframe', 'table')
        if group == 7:
            table = get_html(df.rename(columns=SHOW_COLS_EMP))
        else:
            table = get_html(df.rename(columns=SHOW_COLS))
        return table


def get_date_list():
    df = pd.read_sql("select distinct years, months from cp_result", engine)
    df['dt'] = df.years.astype(str) + df.months.astype(str).str.pad(2, 'left', '0')
    return list(df.dt.values)


DEP_FRAM = {}


class Tree:
    def __init__(self, id, departmentname):
        self.id = id
        self.departmentname = departmentname
        self.parent = []
        self.offspring = {}

    def add_parent(self, supdepid):
        self.parent.append(supdepid)

    def add_offspring(self, id, departmentname):
        if id not in DEP_FRAM:
            DEP_FRAM.setdefault(id, Tree(id, departmentname))
        self.offspring[id] = DEP_FRAM[id]

    def print_offsprings(self, id=None, pre_fix=''):
        print(pre_fix + self.departmentname)
        pre_fix += '+'
        for key in self.offspring:
            self.offspring[key].print_offsprings(pre_fix=pre_fix)

    def get_offsprings(self, id=None, pre_fix=''):
        res = [(self.id, pre_fix + self.departmentname)]
        pre_fix += '+'
        for key in self.offspring:
            res.extend(self.offspring[key].get_offsprings(pre_fix=pre_fix))
        return res


def get_department_framework():
    df = pd.read_sql('''
    SELECT id,departmentname,supdepid FROM hrmdepartment
    where canceled is null
    ''', engine)
    global DEP_FRAM
    DEP_FRAM = {0: Tree(0, 'ALL')}

    for i, (id, dep, sup) in df.iterrows():
        DEP_FRAM[id] = Tree(id, dep)

    for i, (id, dep, sup) in df.iterrows():
        if sup not in DEP_FRAM: continue
        DEP_FRAM[sup].add_offspring(id, dep)
    return DEP_FRAM


def get_auth_department():
    df = pd.read_sql(f'''
    select loginid,departmentid from permission
    ''', engine)
    auth_list = df.groupby('loginid').agg(list).to_dict()['departmentid']
    # df = df.set_index('loginid')
    # return df.to_dict()['departmentid']
    return auth_list


# 权限控制
def has_auth(user, name):
    # 同一个人
    # 拥有部门权限的人
    return True


def get_sup_dep_loginId():
    df = pd.read_sql('''
    select loginid, supdepId from a_CpYgDepBind sup
    inner join HrmResource h on sup.childId=h.departmentid
    ''', engine)

    sup_dep = {l: d for l, d in df.values}
    return sup_dep


def get_dep_loginId():
    df = pd.read_sql('''
    select loginid, departmentid from HrmResource
    ''', engine)

    loginId_dep = {l: d for l, d in df.values}
    return loginId_dep


def get_sup_dep():
    df = pd.read_sql('''
    select childId, supdepId from a_CpYgDepBind
    ''', engine)

    sup_dep = {l: d for l, d in df.values}
    return sup_dep


def get_sup_permission():
    df = pd.read_sql('''
    select loginid, departmentid from sup_permission
    ''', engine)

    sup_permission = df.groupby('loginid').agg(list).to_dict()['departmentid']
    # sup_dep = {l:d for l,d in df.values}
    return sup_permission


def get_loginid_group():
    df = pd.read_sql('''
    select loginid, category from
    (select loginid, category,
           row_number() over (partition by loginid, category order by years desc, months desc) rn
    from result_all) A
    where rn = 1
    ''', engine)
    return dict(df.values)
