# -*- coding:utf-8 -*-
"""
author: byangg
datettime: 2020/3/19 11:34
"""


from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    # path('accounts/login/', views.accounts_login),
    # path('accounts/logout/', views.accounts_logout),
]

