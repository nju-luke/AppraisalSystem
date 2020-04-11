from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Permission
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

perm = 'add_logentry'
permission = Permission.objects.get(codename=perm)

def home(request):
    return render(request,'home.html')

def register(request):
    return render(request, 'uindex.html', context={'register':'ok'})

def register_admin(request):
    return render(request, 'uindex.html', context={'admin':'ok'})


def login_v(request):
    try:
        if request.method == 'GET':
            return render(request, 'uindex.html', {'login': 'OK'})
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.get(username=username)
        if user:
            login(request, user)
            return render(request, 'status.html', {'return_text':'登录成功！'})
    except Exception as e:
        return HttpResponse(e)


def create_user(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        return render(request, 'status.html', {'return_text':'注册成功！'})
    except Exception as e:
        return HttpResponse(e)

def create_admin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.create_user(username=username, password=password)
    # permission = Permission.objects.get(codename='test_view')  # 得到权限
    user.user_permissions.add(permission)                   # 为管理员添加权限
    return render(request, 'status.html', {'return_text':'注册成功！'})

def status(request):
    if request.session.session_key:
        user = request.user
        if user.has_perm('admin.add_logentry'):     # permission.content_type.app_label + permission.codename ??
            return HttpResponse('拥有权限！')
        return HttpResponse('您的账号无权限！')
    else:
        return HttpResponse('未登录！')

@login_required(login_url='login')
def login_view(request):
    return render(request, 'perm_view.html', {'return_text': '看到这个页面，是因为你已经登录了'})

@permission_required('admin.add_logentry')
def permission_view(request):
    return render(request, 'perm_view.html', {'return_text': '看到这个页面，是因为你拥有权限'})

def logout_view(request):
    try:
        # 清空所有权限:
        request.user.user_permissions.clear()
        # 清空会话
        logout(request)
        return HttpResponse('成功退出！')
    except Exception as e:
        return HttpResponse('您未登录！')

@login_required(login_url='login')
def change_pwd(request):
    if request.method == 'GET':
        return render(request, 'uindex.html', {'change': 'ok'})
    new_pwd = request.POST['password']
    request.user.set_password(new_pwd)
    return HttpResponse('密码修改成功!')