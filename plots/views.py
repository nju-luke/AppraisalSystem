from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from plots.plots import get_date_list
from . import plots

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
def charts(request):
    name = request.user.username
    graphJason = charts_gallery.get_chart(name = name, month='2020-01')
    return render(request, 'charts.html', {'plot':graphJason})

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