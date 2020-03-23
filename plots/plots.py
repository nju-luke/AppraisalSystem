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


def get_data(month):
    sql = f'''
            SELECT 
                name,substr(date,1,7) mon, 
                avg(score) score, 
                avg(point) point
            FROM appraisal.data
            where substr(date,1,7) = '{month}'
            group by substr(date,1,7),name
            '''
    df = pd.read_sql(sql, engine)
    area1_x, area1_y, area2_x, area2_y = get_area(df)
    return df, area1_x, area1_y, area2_x, area2_y


def get_base_chart(month):
    df, area1_x, area1_y, area2_x, area2_y = get_data(month)
    point = go.Scatter(x=df.score, y=df.point, mode='markers + text',
                       text=df.name, textposition='top center')
    area1 = go.Scatter(x=area1_x, y=area1_y, line_color='LightSalmon',
                       mode='lines', fill='toself', name='warn')
    area2 = go.Scatter(x=area2_x, y=area2_y, line_color='lightskyblue',
                       mode='lines', fill='toself', name='perf')

    fig = go.Figure([area1, area2, point])
    fig.update_layout(showlegend=False)
    return fig


class ChartsGallery():
    charts = {}

    def _initialize_chart(self, month):
        chart = get_base_chart(month)
        self.charts[month] = chart

    def _get_auth(self, username):
        pass

    def get_chart(self, name, month):
        if not month in self.charts:
            self._initialize_chart(month)
        chart = deepcopy(self.charts[month])  # todo 是否需要copy

        # todo 修改用户显示数据
        if name:
            text = [n if n == name else None for n in chart.data[2].text]
            chart.data[2].update({'text': text})

        graphJason = json.dumps(chart, cls=PlotlyJSONEncoder)
        return graphJason


def get_date_list():
    df = pd.read_sql('''
    select distinct `timestamp` as dt from data
    ''', engine)
    return list(df.dt.values)