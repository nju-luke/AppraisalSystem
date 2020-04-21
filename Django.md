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
    
    user = authenticate(request, username=username, password=password) # 如果存在，则返回用户User，不存在返回None
    # user = User.objects.get(username=username)
    if user:
        login(request, user)
        if user.has_perm('admin.add_logentry'):     # permission.content_type.app_label + permission.codename ??
            return HttpResponse('拥有权限！')
```

## django session
> django 可通过session保存当前登录的信息
```python
request.session['args'] = {'key1':'value1'}
```

## centos 中django使用mssql
> django 本身是支持mysql等数据库的，但不支持microsoft sql server
1. 安装相关驱动
    ```sh
    mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo_bak \
    && echo y|curl http://mirrors.163.com/.help/CentOS7-Base-163.repo > /etc/yum.repos.d/CentOS-Base.repo \
    && yum clean all \
    && yum makecache

   curl https://packages.microsoft.com/config/rhel/7/prod.repo > /etc/yum.repos.d/mssql-release.repo \
   && echo y|yum update \
   && echo y|ACCEPT_EULA=Y yum install -y msodbcsql-13.0.1.0-1 mssql-tools-14.0.2.0-1 \
   && echo y|yum install unixODBC-utf16-devel \
   && ln -sfn /opt/mssql-tools/bin/sqlcmd-13.0.1.0 /usr/bin/sqlcmd  \
   && ln -sfn /opt/mssql-tools/bin/bcp-13.0.1.0 /usr/bin/bcp \
   && echo y|yum install gcc-c++ \
   && echo y|yum install python-devel
    ```
2. 安装pip包
    ```shell script
    pip isntall pyodbc Django==3.0.4 django-mssql-backend
    ```
3. 配置
    ```python
    DATABASES = {
        'default': {
            'ENGINE' : 'sql_server.pyodbc',
            'NAME' : 'ecology',
            'HOST' : 'localhost',
            'PORT' : 1433,
            'USER' : 'sa',
            'PASSWORD' : 'Do8gjas07gaS1',
            'OPTIONS': {
                'DRIVER': 'SQL Server',
               },
           }
    }
    ```

## View的两种定义方式
urls中的两种使用方式：
```python
    path('chgpwd/', views.chgpwd, name='chgpwd'),
    path('test/', views.TestView.as_view(), name='test'),
```
1. 函数式
    ```python
    @login_required(login_url='login')
    def chgpwd(request):
        if request.method == "GET":
    ```
    通过装饰器指定权限，通过判断method确定是GET还是POST
2. 对象式
    ```python
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
    ```
    通过Mixin指定权限，（暂未使用其他权限，不知如何指定？）
    通过 get 与 post方法，确定逻辑

## urls 中 name的使用
```python
path('chgpwd/', views.chgpwd, name='chgpwd'),
```
1. views代码中
    ```python
    reverse("chgpwd")
    ```
2. html中
    ```html
    href="{% url 'manager' %}"
    ```

## 使用企业微信认证登录
判断是否登录 ——》 获取code ——》获取token ——》获取用户名 ——》登录
```python

def ewechat(request):
    if request.session.session_key:
        HttpResponseRedirect(reverse("charts"))

    if request.user.is_anonymous and 'code' not in request.GET:
        target_url = request.META["HTTP_HOST"] + reverse("ewechat")
        url_unlogin = f"https://open.weixin.qq.com/connect/oauth2/authorize?appid={corpid}&redirect_uri={target_url}" \
                      "&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect"
        return HttpResponseRedirect(url_unlogin)

    code = request.GET['code']

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

    return HttpResponseRedirect(reverse("charts"))
```

## 下拉框
1. html
    ```html
    {% for dt in date_list %}
    <option id="dt" value="{{ dt }}" {%if select_month == dt%} selected {%endif%}>{{ dt }}</option>
    {% endfor %}
    ```

## plotly js 作图
后台返回的参数
```python
area1_x, area1_y, area2_x, area2_y,area3_x, area3_y,area4_x, area4_y  = areas
area1 = go.Scatter(x=area1_x, y=area1_y, line_color=colors[3],fillcolor=colors[3],
                   mode='lines', fill='toself', name='Perfect')
fig = go.Figure([area1, point])
graphJason = json.dumps(fig, cls=PlotlyJSONEncoder)
```
前端作图代码， 引用js plotly-latest.min.js
```html
<!--<script src="../../static/js/plotly-latest.min.js"></script>--> <!-- 注意路径 -->

<div class="container">
    <div class="row">
        <div class="col-md-12">
            <div class="chart" id="bargraph">
                <script>
                var graphs = {{plot | safe}};
                Plotly.plot('bargraph',graphs,{});
                </script>
            </div>
        </div>
    </div>
</div>
```


## plotly
1. 通过url实现点击text跳转到指定网页
    ```python
        df['url'] = "<a href='/appraisal/dtl?name=" + df.loginid + f"&month={month}" \
                    + f"&group={group}" + f"&depart={depart}" + "'>" + df.lastname + "</a>"
        point = go.Scatter(x=df.score1, y=df.point1, mode='markers + text', marker=dict(color='blue'),
                           text=df.url, textposition='top center', # 显示在点上方的文字
                           hovertext=df['hover_txt'],   # 鼠标移到点上以后显示的文字
                           hoverinfo='text'
                           )
    ```
2. 面积图
    ```python
        area3 = go.Scatter(x=area3_x, y=area3_y, line_color=colors[1], fillcolor=colors[1],
                           mode='lines', fill='toself', name='Normal')
        area4 = go.Scatter(x=area4_x, y=area4_y, line_color=colors[0], fillcolor=colors[0],
                           mode='lines', fill='toself', name='Pool')
    ```


## pandas 操作
1. to_html, 修改表格
    ```python
        html = df.to_html(index=False, classes='table-striped', border=0).replace(
            'dataframe', 'table').replace('<tr>', '<tr style=" white-space:nowrap" class="text-center">').\
            replace('<tr style="text-align: right;">','<tr style=" white-space:nowrap" class="text-center">')
    ```
2. to_sql, 指定类型
    ```python
        from sqlalchemy import NVARCHAR
        df.to_sql('result_all', engine, if_exists='replace', index=False,
                  dtype={'lastname': NVARCHAR('max'), 'supName': NVARCHAR('max'),
                         'departmentname': NVARCHAR('max')})  # todo 修改为append
    ```
3. 修改部分列名
    ```python
    SHOW_COLS = {"name": "姓名"}
    df = df.rename(columns=SHOW_COLS)
    ```

