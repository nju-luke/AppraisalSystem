# -*- coding:utf-8 -*-
"""
author: byangg
datettime: 2020/3/20 14:00
"""
import json
import string
from copy import deepcopy

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from _plotly_utils.utils import PlotlyJSONEncoder
from plotly.offline import plot
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:00000@localhost:3306/appraisal')

TABLE_COLS = ['lastname', 'score', 'point', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'num']


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
    xs = np.quantile(df.score, [0, 0.25, 0.5, 0.75, 1])
    ys = np.quantile(df.point, [0, 0.25, 0.5, 0.75, 1])

    xs[0] -= 5
    xs[-1] += 5
    ys[0] -= 5
    ys[-1] += 5

    area1_x = [xs[0], xs[1], xs[1], xs[0], xs[0]]
    area1_y = [ys[0], ys[0], ys[1], ys[1], ys[0]]

    area2_x = [xs[3], xs[4], xs[4], xs[3], xs[3]]
    area2_y = [ys[3], ys[3], ys[4], ys[4], ys[3]]

    return area1_x, area1_y, area2_x, area2_y


def get_data(month, categoty):
    year = int(month[:4])
    month = int(month[5:])
    sql = f'''
        select loginid,
               lastname,
               total score, point, 
               v1 ,v2 ,v3 ,v4 ,v5 ,v6 ,v7 ,v8 ,v9 ,v10,v11,
               departmentid,
               row_number() over (order by total desc) num
        from ecology.cp_result where years={year} and months={month}
        and category={categoty}
            '''
    df = pd.read_sql(sql, engine)
    area1_x, area1_y, area2_x, area2_y = get_area(df)
    return df, area1_x, area1_y, area2_x, area2_y


def get_base_chart(month, group):
    df, area1_x, area1_y, area2_x, area2_y = get_data(month, group)
    df['url'] = "<a href='/dtl/?name=" + df.loginid + f"&month={month}" \
                + f"&group={group}" + "'>" + df.lastname + "</a>"
    point = go.Scatter(x=df.score, y=df.point, mode='markers + text',
                       text=df.url, textposition='top center')
    area1 = go.Scatter(x=area1_x, y=area1_y, line_color='LightSalmon',
                       mode='lines', fill='toself', name='warn')
    area2 = go.Scatter(x=area2_x, y=area2_y, line_color='lightskyblue',
                       mode='lines', fill='toself', name='perf')

    fig = go.Figure([area1, area2, point])
    fig.update_layout(showlegend=False)
    return df, fig


class ChartsGallery():
    charts = {}
    dataframes = {}

    def _initialize_chart(self, month, group):
        df, chart = get_base_chart(month, group)
        self.charts[(month, group)] = chart
        self.dataframes[(month, group)] = df

    def _get_department_auth(self, username):
        # todo 权限
        pass

    def get_chart(self, name, month, department=None, group=None):

        if not (month, group) in self.charts:
            self._initialize_chart(month, group)
        chart = deepcopy(self.charts[(month, group)])  # todo 是否需要copy

        # todo 处理部门数据
        # todo 部门权限

        if not department:
            indices = list(self.dataframes[(month, group)].loginid == name)
        else:
            indices = list(self.dataframes[(month, group)].departmentid == int(department))
        # text = [n if n == name else None for n in chart.data[2].text]
        text = [self.dataframes[(month, group)].url[i] if v else None for i, v in enumerate(indices)]
        # text = [f"<a href='https://google.com'>{n}</a>" if n == name else None for n in chart.data[2].text]
        chart.data[2].update({'text': text})
        graphJason = json.dumps(chart, cls=PlotlyJSONEncoder)
        return graphJason

    def get_chart_and_dtl(self, name, month, group=7):
        # todo 只显示个人信息
        graph = self.get_chart(name, month, group=group)
        table = self.dataframes[(month, group)][self.dataframes[(month, group)].loginid == name][TABLE_COLS]. \
            to_html(index=False).replace('dataframe', 'table')
        return graph, table


def get_date_list():
    df = pd.read_sql('''
    select distinct concat(years, lpad(months,2,'0')) dt from ecology.cp_result
    ''', engine)
    return list(df.dt.values)


# def get_auth_department(user=None):
#     # todo 权限
#     df = pd.read_sql('''
#     SELECT id,departmentname FROM ecology.hrmdepartment
#     where canceled is null
#     ''', engine)
#
#     return [(id, dp) for id, dp in df.values]


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
        if id:
            print(pre_fix + self.offspring[id].departmentname)
            if self.offspring[id].offspring:
                for key in self.offspring[id].offspring:
                    self.offspring[id].offspring[key].print_offsprings(pre_fix=pre_fix)
        else:
            print(pre_fix + self.departmentname)
            pre_fix += '  '
            for key in self.offspring:
                self.print_offsprings(id=key, pre_fix=pre_fix)

    def get_offsprings(self, id=None, pre_fix=''):
        res = []
        if id:
            res.append((id, pre_fix + self.offspring[id].departmentname))
            if self.offspring[id].offspring:
                for key in self.offspring[id].offspring:
                    res += self.offspring[id].offspring[key].get_offsprings(pre_fix=pre_fix)
        else:
            res.append((self.id, pre_fix + self.departmentname))
            pre_fix += '  '
            for key in self.offspring:
                res += self.get_offsprings(id=key, pre_fix=pre_fix)
        return res


def get_department_framework():
    df = pd.read_sql('''
    SELECT id,departmentname,supdepid FROM ecology.hrmdepartment
    where canceled is null
    ''', engine)
    DEP_FRAM = {0: Tree(0, 'ALL')}

    for i, (id, dep, sup) in df.iterrows():
        DEP_FRAM[id] = Tree(id, dep)

    for i, (id, dep, sup) in df.iterrows():
        if sup not in DEP_FRAM: continue
        DEP_FRAM[sup].add_offspring(id, dep)
    return DEP_FRAM

def get_auth_department():
    df = pd.read_sql(f'''
    select loginid,departmentid from ecology.permission
    ''', engine)
    df = df.set_index('loginid')
    return df.to_dict()['departmentid']

# 权限控制
def has_auth(user, name):
    return True
