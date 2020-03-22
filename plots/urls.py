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
    path('stuff/', views.stuff_vew, name='stuff'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('chgwd/', views.chgwd, name='chgwd'),


]

