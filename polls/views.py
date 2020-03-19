#导入Userm model 和 权限 相关的包
from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User, Permission, ContentType
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import  authenticate,login,logout
# from .models import Alter

# 用户登录页面
def index(request):
    return render(request,'index.html')

# 用户注册页面
def register(request):
    return render(request,'index.html',{'register':'ok'})

# 注册
def registerview(request):
    username = request.POST['username']
    password = request.POST['password']
    User.objects.create_user(username=username, password=password)
    print('注册成功！')
    return render(request,'index.html')


# 用户登录验证
def loginview(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username,password=password)
    # authenticate 如果用户名密码都正确，返回一个对象,否则返回None
    if user is not None:
        login(request,user)  #保存登录会话,将登陆的信息封装到request.user,包括session
        return HttpResponse('登录成功！')
    else:
        return render(request, 'index.html',{'error':'用户名户密码错误！'})




# 管理员注册页
def register_admin(request):
    return render(request,'index.html',{'admin':'ok'})

# 管理员注册
def admin_view(request):
    '''
    为管理员注册，并赋予权限
    :param request:
    :return:
    '''
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.create_user(username=username, password=password)
    # user.has_perm('Login.change_alter')  #这是用来缓存权限的
    '''
    #这里是创建自定义权限，详情看下章。。。
    content_type = ContentType.objects.get_for_model(Alter) 
    Permission.objects.create(codename='can_alter',content_type=content_type)
    # 注意这里的codename值不是随便命名,是Login这个app下的有个Alter模型
    '''
    permission = Permission.objects.get(codename='change_alter')  # 得到权限
    user.user_permissions.add(permission)                   # 为管理员添加权限
    print('管理员注册成功！')
    return render(request, 'index.html')

# 用户登录检测
@login_required(login_url='index')  #如果未登录则重定向到url：index路径下
def alter(request):
    return HttpResponse('我是修改内容！')

# 管理员权限
@permission_required('Login.change_alter')#,login_url='alter')
def alter_admin(request):
    user = User.objects.get(username=request.user)
    # print(user.has_perm('Login.change_alter'))  #True
    return HttpResponse('管理员才能看见！')

# 退出，清除浏览器会话
def logout_view(request):
    # 清空所有权限:
    request.user.user_permissions.clear()
    # 清空会话
    logout(request)
    return HttpResponse('成功退出！')


