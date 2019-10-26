from django.db import models

# Create your models here.


class Finger(models.Model):
    url = models.CharField(max_length=32,verbose_name='url指纹')
    is_active = models.BooleanField(default=True,verbose_name='是否可用')


    class Meta:
        db_table = 'finger'


class SpiderTask(models.Model):
    type = models.CharField(max_length=10,verbose_name='资源类型')
    keyword = models.CharField(max_length=50,verbose_name='查询关键字')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
