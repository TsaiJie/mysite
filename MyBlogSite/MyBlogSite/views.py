from django.shortcuts import render


# 首页
def home(request):
    context = {}
    return render(request, 'home.html', context)
