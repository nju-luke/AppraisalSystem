# -*- coding:utf-8 -*-
"""
author: byangg
datettime: 2020/3/19 11:34
"""


from django.urls import path

from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('login/', views.login_v, name='login'),
    path('register/',views.register,name='register'),
    path('create/',views.create_user,name='create'),

    path('register_admin/',views.register_admin,name='register_admin'),
    path('create_admin/',views.create_admin,name='create_admin'),

    path('status/',views.status,name='status'), ## 查看用户当前状态

    path('login_view/', views.login_view, name='login_view'),   ## 需要登录才能访问
    path('permission_view/',views.permission_view, name='permission_view'),## 需要权限才能访问


    path('change/',views.change_pwd,name='change'), # 用户退出
    path('logout/',views.logout_view,name='logout'), # 用户退出
]

