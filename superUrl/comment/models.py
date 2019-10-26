from django.db import models

# Create your models here.

class Comment(models.Model):
    url = models.CharField(max_length=1000, verbose_name='电影资源链接',null=False)
    phonenumber=models.CharField(max_length=500,verbose_name='电话',null=False)
    content=models.CharField(max_length=1000,verbose_name='电影评论',null=False)
    createtime=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    class Meta:
        db_table='comment'
