from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

from read_statistics.models import ReadNum
from django.contrib.contenttypes.models import ContentType

from django.db.models.fields import exceptions


# Create your models here.

class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


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
