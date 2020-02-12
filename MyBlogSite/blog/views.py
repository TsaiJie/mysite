from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType


# Create your views here.
# 获取所有的博客进行显示
def blog_list(request):
    context = {}
    context['blogs'] = Blog.objects.all()
    return render(request, 'blog_list.html', context)


# 根据博客的id获取对应博客数据，并且渲染出来
def blog_detail(request, blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog, pk=blog_pk)
    return render(request, 'blog_detail.html', context)


def blogs_with_type(request, blog_type_pk):
    context = {}
    print(blog_type_pk)
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_type'] = blog_type
    return render(request, 'blog_with_type.html', context)
