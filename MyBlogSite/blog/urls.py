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
