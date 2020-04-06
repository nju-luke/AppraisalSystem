from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from plots.plots import get_date_list
from . import plots

import datetime

# Create your views here.

charts_gallery = plots.ChartsGallery()

# class IndexView(TemplateView):
#     template_name = "index.html"

def index_view(request):
    if not request.session.session_key:
        return render(request, 'index.html')
    return HttpResponseRedirect('/charts')     # todo 修改跳转页
    # return HttpResponse('''您已登录，<a href=http://127.0.0.1:8000/logout>退出</a>''')

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
            return render(request, 'index.html', {'error':'用户名或密码不正确！'})
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
        return render(request, 'chgpwd.html', {'error':'请输入正确的原始密码！'})
    new_pwd = request.POST['newpwd']
    user.set_password(new_pwd)
    user.save()

    return  render(request, 'chgpwd.html', {'error':'密码修改成功！'})

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


@login_required(login_url='login')
def charts(request):
    name = request.user.username
    month = datetime.date.today().strftime('%Y-%m')
    # todo, 修改日期，获取权限,  #此处根据员工是否领导，直接跳转到可选页面，以及dtl
    is_manager = False
    if not is_manager:
        return HttpResponseRedirect(f"/dtl?name={name}&month={month}")
    # graphJason = charts_gallery.get_chart(name = name, month=month) # todo 修改日期, 根据用户名，找到对应的chart
    # return render(request, 'charts.html', {'plot':graphJason, 'manager': is_manager})
    return HttpResponseRedirect("/manager")

@login_required(login_url='login')
def employee(request):
    # selected = request.GET['selected']
    name = 'songchen'
    is_manager = True
    graphJason = charts_gallery.get_chart(name = name, month='2020-03') # 修改日期
    ## todo 修改颜色
    # return graphJason
    return render(request, 'charts.html', {'plot':graphJason, 'manager': is_manager})

@login_required(login_url='login')
def manager(request):
    # selected = request.GET['selected']
    name = 'huangyouhua'
    is_manager = True
    graphJason = charts_gallery.get_chart(name = name, month='2020-03') # 修改日期
    # return graphJason
    return render(request, 'charts.html', {'plot':graphJason, 'manager': is_manager})


# 权限控制
def has_auth(user, name):

    return True

def dtl(request):
    name = request.GET['name']
    month = request.GET['month']
    if not has_auth(request.user, name):
        return HttpResponse('没有权限！')

    graphJason, table = charts_gallery.get_chart_and_dtl(name = name, month = month)
    # obj = charts_gallery.get_chart_and_dtl(name = name)
    # return HttpResponse(obj)
    return render(request, 'charts.html', {'plot':graphJason, 'table': table})




def test(request):
    if request.method == "GET":
        date_list = get_date_list()
        # data = [1,2,3,4,5]
        return render(request, 'test.html', {'date_list':date_list})

    else:
        select_month = request.POST['select_month']

        return render(request, 'test.html', {'select_month':select_month})

class TestView(View):
    date_list =  get_date_list()
    def get(self, request):

        # date_list =
        # data = [1,2,3,4,5]
        return render(request, 'test.html', {'date_list': self.date_list})

    def post(self, request):
        select_month = request.POST['select_month']
        return render(request, 'test.html', {'select_month':select_month,
                                             'date_list': self.date_list})