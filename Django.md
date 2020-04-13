# Django
django中使用MTV的设计模式：

1. 通过urls找到对应的控制函数
2. views中控制的函数控制逻辑（跳转到html页面，modes中存取用户和数据）
3. templates中定义html

> 一种设计步骤：在view中定义逻辑，确定需要的template并生成html；将view中的逻辑函数映射到urls中。

![image-20200320111819524](D:\Projects\AppraisalSystem\Django_assets\image-20200320111819524.png)

## 新建

### 新建项目

```shell
django-admin startproject AppraisalSystem
cd HelloWorld
python manage.py runserver 0.0.0.0:8000
```

### 新建应用

```sh
python manage.py  startapp mytest
```

## 添加

### 添加app到project

在AppraisalSystem/settings.py中修改

```python
INSTALLED_APPS = [
    'mytest',
    ...
]
```


### 添加第一个view

mytest/view.py

```python
def home(request):
    return render(request,'home.html')
```

mytest/templates/index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Start From Here</title>
</head>
<body>
<div class="connect">
    <p>
        <a class="facebook" href="{% url 'login' %}">登录</a>
    </p>
    <p>
        <a class="facebook" href="{% url 'register' %}">注册</a>
    </p>
    <p>
        <a class="facebook" href="{% url 'register_admin' %}">管理员注册</a>
    </p>
    <p>
    <a class="facebook" href="{% url 'logout' %}">退出</a>
    </p>
    <p>
    <a class="facebook" href="{% url 'login_view' %}">登录访问页面</a>
    </p>
    <p>
    <a class="facebook" href="{% url 'permission_view' %}">有权限的页面</a>
    </p>
</div>

</body>
</html>
```


### 添加app的urls到settings中

在AppraisalSystem/urls.py中修改

```python

urlpatterns = [
    path('mytest/', include('mytest.urls')),
    ...
]
```

在mytest/urls.py中修改
```python
urlpatterns = [
    path('', views.home,name='home'),
    ...
]
```

> 到此，启动服务器后，127.0.0.1:8000/mytest 即可访问到home.html


## 用户管理

### 新建用户
```python
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.create_user(username=username, password=password)
```
### 分配权限
```python
perm = 'add_logentry'
permission = Permission.objects.get(codename=perm)
user.user_permissions.add(permission)  # permission.content_type.app_label + permission.codename ??
```

### 用户登录与权限认证
```python
    user = User.objects.get(username=username)
    if user:
        login(request, user)
        if user.has_perm('admin.add_logentry'):     # permission.content_type.app_label + permission.codename ??
            return HttpResponse('拥有权限！')
```


### centos 中django使用odbc
1. 安装pyodbc
    ```shell script
    yum install unixODBC unixODBC-devel
    yum install gcc-c++
    yum install python-devel
    pip install pyodbc
    ```
2. pip install django-mssql-backend