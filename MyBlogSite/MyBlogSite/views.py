import datetime
from django.db.models import Sum
from django.shortcuts import render, redirect

from blog.models import Blog
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from django.contrib.contenttypes.models import ContentType

from django.utils import timezone
from django.core.cache import cache
from django.contrib import auth
from django.urls import reverse


def get_7_data_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
        .filter(read_details__date__lt=today, read_details__date__gte=date) \
        .values('id', 'title') \
        .annotate(read_num_sum=Sum('read_details__read_num')) \
        .order_by('-read_num_sum')
    return blogs[:7]


# 首页
def home(request):
    # 获取7天热门博客的缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_data_hot_blogs()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 60)
        print('计算缓存')
    else:
        print('use 缓存')
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    today_hot_data = get_today_hot_data(blog_content_type)
    yesterday_hot_data = get_yesterday_hot_data(blog_content_type)

    context = {'read_nums': read_nums, 'dates': dates, 'today_hot_data': today_hot_data,
               'yesterday_hot_data': yesterday_hot_data, 'hot_blogs_for_7_days': hot_blogs_for_7_days}
    return render(request, 'home.html', context)


def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)
    # 获取请求头的信息
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    if user is not None:
        auth.login(request, user)
        return redirect(referer)
    else:
        return render(request, 'error.html', {"message": "用户名或密码不正确"})
