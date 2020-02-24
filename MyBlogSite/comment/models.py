from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.DO_NOTHING)
    # 存放该条评论的父类id，父类可能是评论 可能是回复 指向自己
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.DO_NOTHING)
    # 一条评论下面所有的回复
    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.DO_NOTHING)
    # reply_to 回复谁的 回复哪一条评论的
    reply_to = models.ForeignKey(User, related_name='replies', null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-comment_time']
