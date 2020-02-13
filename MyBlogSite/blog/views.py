from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType
from django.conf import settings
# 引入分页器
from django.core.paginator import Paginator


# Create your views here.
# 获取所有的博客进行显示
def blog_list(request):
    # 获取所有的博客
    blogs_all_list = Blog.objects.all()
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

    context = {}
    # 获取页码值
    context['page_range'] = page_range
    context['blogs'] = page_of_blogs
    # 获取当前页所有的博客
    context['page_of_blogs'] = page_of_blogs
    # 获取所有的博客类型
    context['blog_types'] = BlogType.objects.all()
    return render(request, 'blog_list.html', context)


# 根据博客的类型id获取该篇博客类型对应的所有博客，并且渲染出来
def blogs_with_type(request, blog_type_pk):
    context = {}

    # 获取id=blog_type_pk的博客类型
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    # 获取所有的博客
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)

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

    # 获取页码值
    context['page_range'] = page_range
    context['blogs'] = page_of_blogs
    # 获取当前页所有的博客
    context['page_of_blogs'] = page_of_blogs
    # 获取所有的博客类型
    context['blog_types'] = BlogType.objects.all()
    # 当前博客类型
    context['blog_type'] = blog_type
    return render(request, 'blog_with_type.html', context)


# 根据博客的id获取对应博客数据，并且渲染出来
def blog_detail(request, blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog, pk=blog_pk)
    return render(request, 'blog_detail.html', context)
