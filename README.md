# mysite
使用Django搭建博客

### 环境配置

```powershell
virtualenv mysite_env 
ativate #激活虚拟环境
pip install Django==2.0
deactivate #退出虚拟环境
```

```powershell
# 创建Django项目
django-admin startproject mysite
# 创建blog应用
python manage.py startapp blog 
# 创建两个models 然后进行初始化
python manage.py migrate
# 创建超级管理员
python manage.py createsuperuser
```

```python
# 在setting中加入应用
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
]
# 数据库配置
# setting中设置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysitedb',
        'USER': 'root',
        'PASSWORD': '5211314cmj',
        'HOST': 'localhost',
        'PORT': 3306
    }
}
```

```powershell
# 创建数据库迁移文件 然后迁移
python manage.py makemigrations
python manage.py migrate
```

```python
# admin中注册
from django.contrib import admin
from .models import Blog, BlogType
# Register your models here.


# 注册
@admin.register(BlogType)    
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','content','blog_type','created_time','last_updated_time',)

```

### url 的基本配置

```python
from django.contrib import admin
from django.urls import path, re_path
from . import views

# /blog
urlpatterns = [
    # /blog/1
    path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
    path('type/<int:blog_type_pk>', views.blogs_with_type, name="blogs_with_type"),
    path('', views.blog_list, name="blog_list")
]

```
### views基本配置

```python
from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType


# Create your views here.
# 获取所有的博客进行显示
def blog_list(request):
    context = {}
    context['blogs'] = Blog.objects.all()
    return render(request, 'blog/blog_list.html', context)


# 根据博客的id获取对应博客数据，并且渲染出来
def blog_detail(request, blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog, pk=blog_pk)
    return render(request, 'blog/blog_detail.html', context)


def blogs_with_type(request, blog_type_pk):
    context = {}
    print(blog_type_pk)
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_type'] = blog_type
    return render(request, 'blog/blog_with_type.html', context)

```

### 二 、页面优化

把页面的相同部分抽取出来作为基础页面，其他页面继承这个页面，只在页面中实现自己的页面部分。

```html
{% extends  'base.html' %}
{% block title %}...{% endblock %}
{% block content %}...{% endblock %}
```

静态文件配置

```python
STATIC_URL = '/static/'
# 设置静态文件的路径
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

```

静态文件加载

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/home.css' %}">
```



