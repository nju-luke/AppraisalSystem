from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request,'home.html')


def login_v(request):
    if request.method == 'GET':
        return render(request, 'index.html', {'login': 'OK'})
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.get_by_natural_key(username)
    if user:
        login(request, user)
        request.session['username']=username   #user的值发送给session里的username
        request.session['is_login']=True   #认证为真
        return render(request, 'status.html', {'return_text':'登录成功！'})

def register(request):
    return render(request, 'index.html', context={'register':'ok'})

def create_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.create_user(username=username, password=password)
    return render(request, 'home.html')

def create_admin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.create_user(username=username, password=password)

    permission = Permission.objects.get(codename='test_view')  # 得到权限
    user.user_permissions.add(permission)                   # 为管理员添加权限
    return render(request, 'home.html')

def status(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.get_by_natural_key(username)
        if user.user_permissions.have('test_view'):
            return HttpResponse('拥有权限！')
        return HttpResponse('无权限！')
    except:
        return HttpResponse('未登录！')



@login_required(login_url='login')
def permission_view(request):
    pass


def logout_view(request):
    # 清空所有权限:
    request.user.user_permissions.clear()
    # 清空会话
    logout(request)
    return HttpResponse('成功退出！')