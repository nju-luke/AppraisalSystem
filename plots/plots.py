# -*- coding:utf-8 -*-
"""
author: byangg
datettime: 2020/3/20 14:00
"""
import json
import string

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
    df = pd.DataFrame(np.random.randn(nums, 2) * 10 + 70, dtype=np.int, columns=['x', 'y'], index=list(range(nums)))

    df['name'] = [f'员工_{string.ascii_uppercase[i]}' for i in range(nums)]
    df = df.groupby(['x', 'y'])['name'].agg(lambda x: ','.join(x)).reset_index()

    df_area = pd.DataFrame([[1, 1, 2, 2, 1], [1, 2, 2, 1, 1]]).T * 10

    df_area1 = df_area.copy()

    df_area[0] += 40
    df_area[1] += 40

    df_area1[0] += 70
    df_area1[1] += 70

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df_area[0], y=df_area[1], line_color='Coral', mode='lines', fill='toself', fillcolor='LightSalmon',
                   name='Warn'))
    fig.add_trace(
        go.Scatter(x=df_area1[0], y=df_area1[1], line_color='lightskyblue', mode='lines', fill='toself', name='Pef'))
    fig.add_trace(go.Scatter(x=df['x'], y=df['y'], text=df['name'], mode='markers + text', textposition='top center'))

    fig.update_layout(showlegend=False, height=800, )

    # fig.show()

    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)

    return graphJSON

    # plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    # return plot_div
