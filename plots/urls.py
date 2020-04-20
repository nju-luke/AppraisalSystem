# -*- coding:utf-8 -*-
"""
author: byangg
datettime: 2020/3/19 11:34
"""


from django.urls import path

from . import views

urlpatterns = [
    # path('', views.IndexView.as_view(),name='index'),
    path('', views.index_view,name='index'),
    # path('stuff/', views.StuffView.as_view(), name='stuff'),
    # path('charts/', views.charts, name='charts'),
    path('dtl/', views.dtl, name='dtl'),
    path('charts/', views.Charts.as_view(), name='charts'),

    path('employee/', views.employee, name='employee'),
    path('manager/', views.manager, name='manager'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('chgpwd/', views.chgpwd, name='chgpwd'),

    path('test/', views.TestView.as_view(), name='test'),
    # path('test/', views.test, name='test'),

    path('ewechat/', views.ewechat, name='ewechat')


]

