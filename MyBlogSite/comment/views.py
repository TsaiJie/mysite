from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from .forms import CommentForm


# Create your views here.

def update_comment(request):
    data = {}
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    # 先把request.user传入实例对象，然后再传入super之前在实例中取出来，
    comment_form = CommentForm(request.POST, user=request.user)
    if comment_form.is_valid():
        # 检查通过，保存数据
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.save()
        # 返回数据
        data['status'] = "SUCCESS"
        data['username'] = comment.user.username
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = comment.text
        # return redirect(referer)
    else:
        # return render(request, 'error.html', {"message": comment_form.errors, "redirect_to": referer})
        data['status'] = "ERROR"
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)
