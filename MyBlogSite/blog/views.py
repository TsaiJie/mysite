from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from read_statistics.utils import read_statistics_once_read
from .models import Blog, BlogType
from django.conf import settings
# 引入分页器
from django.core.paginator import Paginator

from read_statistics.models import ReadNum
from django.contrib.contenttypes.models import ContentType


def get_blog_list_common_data(request, blogs_all_list):
    # 获取页码参数，默认为1
    page_num = request.GET.get("page", 1)
    # 创建分页器实例对象，每10条进行一次分页
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)
    # 获取当前页所有的博客
    page_of_blogs = paginator.get_page(page_num)
    # 获取当前页码
    current_page_num = page_of_blogs.number
    # 获取当前页码的前后两页
    page_range = []
    for i in range(current_page_num - 2, current_page_num + 2 + 1):
        if i <= 0:
            continue
        if i > paginator.num_pages:
            continue
        page_range.append(i)
    # 加上页码省略标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, "...")
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append("...")
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取博客分类的对应博客数量
    """
    blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)
    """
    blog_types_list = BlogType.objects.annotate(blog_count=Count('blog'))
    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    # 获取页码值
    context['page_range'] = page_range
    context['blogs'] = page_of_blogs
    # 获取当前页所有的博客
    context['page_of_blogs'] = page_of_blogs
    # 获取所有的博客类型
    context['blog_types'] = blog_types_list
    context['blog_dates'] = blog_dates_dict
    return context


# Create your views here.
# 获取所有的博客进行显示
def blog_list(request):
    # 获取所有的博客
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog_list.html', context)


# 根据博客的类型id获取该篇博客类型对应的所有博客，并且渲染出来
def blogs_with_type(request, blog_type_pk):
    # 获取id=blog_type_pk的博客类型
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    # 获取所有的博客
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blogs_all_list)
    # 当前博客类型
    context['blog_type'] = blog_type
    return render(request, 'blog_with_type.html', context)


def blogs_with_date(request, year, month):
    # 获取所有的博客
    # mysql中无法同时获取年和月份获取的数据为空，因为不支持TIME_ZONE = 'Asia/Shanghai' 需要把USE_TZ = True 改为False
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_with_date'] = "%s年%s月" % (year, month)
    return render(request, 'blog_with_date.html', context)


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
    read_cookie_key = read_statistics_once_read(request, blog)

    response = render(request, 'blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true')  # 阅读cookie标记
    return response
