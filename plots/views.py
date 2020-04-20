import datetime
import json
from urllib import parse

import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View

from plots.plots import get_date_list, get_auth_department, get_department_framework, get_sup_dep_loginId, \
    get_sup_dep, get_sup_permission, get_dep_loginId
from . import plots

import sys
import os

sys.path.append(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])

from settings import corpid, corpsecret

# Create your views here.


date_list = get_date_list()
department_framework = get_department_framework()
auth_department = get_auth_department()  # 授权的部门
loginId_supdep = get_sup_dep_loginId()  # 登录用户的最高级部门
loginId_dep = get_dep_loginId()  # 登录用户的最高级部门
depart_supdep = get_sup_dep()  # 当前部门的最高级部门
sup_permission = get_sup_permission()  # 最高级权限

charts_gallery = plots.ChartsGallery()
charts_gallery.initialize_chart(max(date_list), 6)
for sup in set(loginId_supdep.values()):
    charts_gallery.initialize_chart_emp(max(date_list), 7, sup)


def index_view(request):
    if not request.session.session_key:
        return render(request, 'index.html')
    return HttpResponseRedirect('/charts')


def login_view(request):
    try:
        if request.method == 'GET':
            return render(request, 'index.html', {'login': 'OK'})
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # user = User.objects.get(username=username)
        if user:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return render(request, 'index.html', {'error': '用户名或密码不正确！'})
    except Exception as e:
        return HttpResponse(e)


@login_required(login_url='login')
def chgpwd(request):
    if request.method == "GET":
        return render(request, 'chgpwd.html')
    username = request.user.username
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if not user:
        return render(request, 'chgpwd.html', {'error': '请输入正确的原始密码！'})
    new_pwd = request.POST['newpwd']
    user.set_password(new_pwd)
    user.save()
    return render(request, 'chgpwd.html', {'error': '密码修改成功！'})


@login_required(login_url='login')
def logout_view(request):
    try:
        # 清空所有权限:
        request.user.user_permissions.clear()
        # 清空会话
        logout(request)
        return HttpResponseRedirect("/")
    except Exception as e:
        return HttpResponse('您未登录！')


class Charts(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user.username
        request.session['args'] = {'date_list': date_list}
        # month = datetime.date.today().strftime('%Y%m')
        month = max(date_list)

        if not user in auth_department:
            group = 7
            depart = loginId_supdep[user]
            return HttpResponseRedirect(f"/dtl?name={user}&month={month}&group={group}&depart={depart}")

        request.session['args']['is_manager'] = True

        # 显示授权的部门
        auth_dep_ids = auth_department[user]
        request.session['args']['department_list'] = []
        for auth_dep_id in auth_dep_ids:
            request.session['args']['department_list'] += department_framework[auth_dep_id].get_offsprings()
        request.session['args']['department_list_ids'] = [id_ for id_, name in request.session['args'][
            'department_list']]
        request.session['args']['select_department'] = auth_dep_ids[0]

        # 显示授权的部门
        try:
            sup_perm_ids = sup_permission[user]
            request.session['args']['sup_perm_list'] = []
            for sup_perm in sup_perm_ids:
                request.session['args']['sup_perm_list'] += department_framework[sup_perm].get_offsprings()
            request.session['args']['sup_perm_list'] = [id_ for id_, name in request.session['args']['sup_perm_list']]
            # request.session['args']['select_department'] = auth_dep_ids[0]
        except KeyError:
            pass

        if request.session['args']['select_department'] == 1:
            request.session['args']['select_department'] = 0  # 默认高管拥有全部权限

        request.session['args']['select_month'] = month
        return self.manager(request)

    def post(self, request):
        select_month = request.POST['select_month']
        request.session['args']['select_month'] = select_month

        if not 'select_group' in request.POST:
            # todo 在别人的详情页查看时，修改前端  request.headers['referer']
            url = request.headers['referer']
            referer_args = dict(parse.parse_qsl(parse.urlsplit(url).query))
            user = referer_args['name']
            group = referer_args['group']
            if group == 6:
                return HttpResponseRedirect(f"/dtl?name={user}&month={select_month}&group={group}")  #
            depart = referer_args['depart']
            return HttpResponseRedirect(f"/dtl?name={user}&month={select_month}&group={group}&depart={depart}")
        try:
            request.session['args']['select_group'] = int(request.POST['select_group'])
            request.session['args']['select_department'] = int(request.POST['select_department'])
            if request.session['args']['select_group'] == 7 and request.session['args']['select_department'] == 0:
                return HttpResponse("请勿同时选择所有部门和员工评分")
            if request.session['args']['select_department'] == 1:
                return HttpResponse("请勿选择总经办")
        except:
            pass

        return self.manager(request)

    def manager(self, request):
        if not 'select_group' in request.session['args']:
            request.session['args']['select_group'] = 6

        if not 'select_department' in request.session['args']:
            request.session['args']['select_department'] = None
            departments = None
            sup_depart = None
        else:
            departments = department_framework[request.session['args']['select_department']].get_offsprings()
            departments = [group[0] for group in departments]  ##获取权限，显示对应数据
            sup_depart = depart_supdep[request.session['args']['select_department']] \
                if not request.session['args']['select_department'] == 0 else 0

        return_kargs = request.session['args']
        graphJason, table = charts_gallery.get_chart(name=request.user.username,
                                                     month=return_kargs['select_month'],
                                                     department=departments,
                                                     group=return_kargs['select_group'],
                                                     sup_depart=sup_depart
                                                     )  # 修改日期
        return_kargs['plot'] = graphJason
        return_kargs['table'] = table
        # return graphJason
        return render(request, 'charts.html', return_kargs)


@login_required(login_url='login')
def charts(request):
    name = request.user.username
    month = datetime.date.today().strftime('%Y-%m')
    # todo, 修改日期，获取权限,  #此处根据员工是否领导，直接跳转到可选页面，以及dtl
    is_manager = True
    if not is_manager:
        return HttpResponseRedirect(f"/dtl?name={name}&month={month}")
    # graphJason = charts_gallery.get_chart(name = name, month=month) # todo 修改日期, 根据用户名，找到对应的chart
    # return render(request, 'charts.html', {'plot':graphJason, 'is_manager': is_manager})
    return HttpResponseRedirect("/manager")


@login_required(login_url='login')
def employee(request):
    # selected = request.GET['selected']
    name = 'songchen'
    is_manager = True
    graphJason, table = charts_gallery.get_chart(name=name, month='2020-03')  # 修改日期
    ## todo 修改颜色
    # return graphJason
    return render(request, 'charts.html', {'plot': graphJason, 'is_manager': is_manager})


@login_required(login_url='login')
def manager(request):
    # selected = request.GET['selected']
    name = 'huangyouhua'
    is_manager = True
    graphJason, table = charts_gallery.get_chart(name=name, month='2020-03')  # 修改日期
    # return graphJason
    return render(request, 'charts.html', {'plot': graphJason, 'is_manager': is_manager})


def dtl(request):
    name = request.GET['name']
    month = request.GET['month']
    group = int(request.GET['group'])
    sup_depart = request.GET['depart']

    dep = loginId_dep[name]
    if name != request.user.username and dep not in request.session['args']['department_list_ids']:
        return HttpResponse('没有权限！')

    is_sup_perm = False
    try:
        if dep in request.session['args']['sup_perm_list']:
            is_sup_perm = True
    except KeyError:
        pass

    # todo 添加明细数据
    graphJason, table, cp_dtl = charts_gallery.get_chart_and_dtl(name=name, month=month, group=group,
                                                                 sup_depart=sup_depart,
                                                                 is_sup_perm=is_sup_perm)
    if request.user.username == name:
        cp_dtl = None
    return render(request, 'charts.html', {'plot': graphJason, 'table': table,
                                           'select_month': month,
                                           'date_list': request.session['args']['date_list'],
                                           'cp_dtl': cp_dtl
                                           }, )


def test(request):
    if request.method == "GET":
        date_list = get_date_list()
        # data = [1,2,3,4,5]
        return render(request, 'test.html', {'date_list': date_list})
    else:
        select_month = request.POST['select_month']
        return render(request, 'test.html', {'select_month': select_month})


class TestView(LoginRequiredMixin, View):
    date_list = get_date_list()
    department_list = get_auth_department()

    def get(self, request):
        return render(request, 'test.html', {'date_list': self.date_list,
                                             'departments': self.department_list
                                             })

    def post(self, request):
        select_month = request.POST['select_month']
        select_department = request.POST['select_department']
        return render(request, 'test.html', {
            'date_list': self.date_list,
            'departments': self.department_list,
            'select_month': select_month,
            'select_department': select_department
        })

def ewechat(request):
    if request.session.session_key:
        HttpResponseRedirect("/charts")

    if request.user.is_anonymous and 'code' not in request.GET:
        target_url = request.path
        url_unlogin = f"https://open.weixin.qq.com/connect/oauth2/authorize?appid={corpid}&redirect_uri={target_url}" \
                      "&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect"
        return HttpResponseRedirect(url_unlogin)

    code = request.GET['code'][0]

    token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}"
    response = requests.post(token_url).text
    ACCESS_TOKEN = json.loads(response)['access_token']

    user_url = f"https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token={ACCESS_TOKEN}&code={code}"
    response = requests.post(user_url).text
    username = json.loads(response)['UserId']

    user = User.objects.get(username=username)

    if user:
        login(request, user)
    else:
        raise ValueError(f'用户名不存在：{username}')

    return HttpResponseRedirect("/charts")

