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

```python
# mysql中无法同时获取年和月份获取的数据为空，因为不支持TIME_ZONE = 'Asia/Shanghai' 需要把USE_TZ = True 改为False
blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
```



## 富文本编辑器

django-ckeditor配置 富文本编辑器

```
1. 安装
pip install django-ckeditor
2.注册
'ckeditor'
3. 配置model
把字段改为RichTextField
```



```python
配置上传图片功能
1. 安装 pip install pillow
2. 注册应用 'ckeditor_uploader'
3. 配置settings 
# 在根目录创建 media文件夹
# media 保存上传的文件
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 配置ckeditor
CKEDITOR_UPLOAD_PATH = 'upload/'
4. 配置url
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    ...
    path('ckeditor', include('ckeditor_uploader.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
5.配置model
from ckeditor_uploader.fields import RichTextUploadingField
content = RichTextUploadingField()
```

### 博客阅读统计

当进入具体一篇博客的时候，判断博客该博客是否拥有COOKIES的值，如果有则不作阅读数量加一的操作，如果没有则做数量加一的操作。

1.简单有bug的阅读统计

```python
# 在blog model中添加了read_num字段
    blog = get_object_or_404(Blog, pk=blog_pk)
    if not request.COOKIES.get('blog_%s_read' % blog_pk):
        blog.read_num += 1
        blog.save()

    response = render(request, 'blog_detail.html', context)
    response.set_cookie('blog_%s_read' % blog_pk, 'true')
    return response
```



2.单独作为一个model

```python
# model中
from django.db.models.fields import exceptions
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    blog = models.OneToOneField(Blog, on_delete=models.DO_NOTHING)
class Blog(models.Model):
    ...
    def get_read_num(self):
        try:
            return self.readnum.read_num
        except exceptions.ObjectDoesNotExist:
            # 如果没有该对象则返回0
            return 0
	...
 
# admin中
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'blog_type', 'get_read_num', 'created_time', 'last_updated_time',)


@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'blog')

 # views中
def blog_detail(request, blog_pk):
    if not request.COOKIES.get('blog_%s_read' % blog_pk):
        if ReadNum.objects.filter(blog=blog).count():
            #  存在记录
            readnum = ReadNum.objects.get(blog=blog)
        else:
            # 不存在记录
            readnum = ReadNum(blog=blog)
        # 计数加一
        readnum.read_num += 1
        readnum.save()

    response = render(request, 'blog_detail.html', context)
    response.set_cookie('blog_%s_read' % blog_pk, 'true')
    return response

```

3.设置为通用的计数模型，可以对任意模型计数

使用ContentType，这个模型关联了我们创建的所有模型

```python
#read_statistics app  的model中

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

```

```python
# blog app 的model中
from read_statistics.models import ReadNum
from django.contrib.contenttypes.models import ContentType

class Blog(models.Model):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def get_read_num(self):
        try:
            # 首先从ContentType中获取blog对象
            ct = ContentType.objects.get_for_model(self)
            # 然后根据获取的对象，在ReadNum进行查找，它的阅读数量对象
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            # 如果没有该对象则返回0
            return 0

    def __str__(self):
        return "<Blog: %s>" % self.title

    #  设置排序规则
    class Meta:
        ordering = ['-created_time']
```

```python
# views中
from read_statistics.models import ReadNum
from django.contrib.contenttypes.models import ContentType

# 根据博客的id获取对应博客数据，并且渲染出来
def blog_detail(request, blog_pk):
    context = {}
    # 当前博客
    blog = get_object_or_404(Blog, pk=blog_pk)
    # 当前博客的上一条博客
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    # 当前博客的下一条博客
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()

    context['blog'] = blog
    blog = get_object_or_404(Blog, pk=blog_pk)
    if not request.COOKIES.get('blog_%s_read' % blog_pk):
        ct = ContentType.objects.get_for_model(blog)
        if ReadNum.objects.filter(content_type=ct, object_id=blog.pk).count():
            #  存在记录
            readnum = ReadNum.objects.get(content_type=ct, object_id=blog.pk)
        else:
            # 不存在记录
            readnum = ReadNum(content_type=ct, object_id=blog.pk)
        # 计数加一
        readnum.read_num += 1
        readnum.save()

    response = render(request, 'blog_detail.html', context)
    response.set_cookie('blog_%s_read' % blog_pk, 'true')
    return response
```

### 使用数据库缓存

https://docs.djangoproject.com/zh-hans/2.2/topics/cache/

```python
# 数据库缓存设置
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}

from django.core.cache import cache

hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_data_hot_blogs()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 60)
        print('计算缓存')
    else:
        print('use 缓存')
```



