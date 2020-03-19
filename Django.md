# Django

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

### 添加app的urls到settings中

在AppraisalSystem/urls.py中修改

```python

urlpatterns = [
    path('mytest/', include('mytest.urls')),
    ...
]
```

### 添加第一个view

mytest/view.py

```python
def index(request):
    return render(request,'index.html')
```

mytest/templates/index.html

```html

```

