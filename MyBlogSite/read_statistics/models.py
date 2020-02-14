from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.db.models.fields import exceptions


# Create your models here.
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class ReadNumExpandMethod(object):
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
