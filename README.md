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

