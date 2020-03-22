from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from . import plots

# Create your views here.

charts_gallery = plots.ChartsGallery()

# class IndexView(TemplateView):
#     template_name = "index.html"

def index_view(request):
    if not request.session.session_key:
        return render(request, 'index.html')
    # return HttpResponseRedirect('/stuff')
    return HttpResponse('''您已登录，<a href=http://127.0.0.1:8000/logout>退出</a>''')

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
def chgwd(request):
    return None

@login_required(login_url='login')
def stuff_vew(request):
    # if request.method == 'GET':
    #     return render(request, 'stuff.html')
    # username = request.user.username
    # graphJason = plots.stuff_plot(username)

    # mon = request.user.username
    try:
        name = request.POST['name']
    except:
        name = None
    graphJason = charts_gallery.get_chart(name = name, month='2020-01')

    return render(request, 'stuff.html', {'plot':graphJason})

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