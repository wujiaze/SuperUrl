from django.db import models

# Create your models here.

class Comment(models.Model):
    url = models.CharField(max_length=1000, verbose_name='电影资源链接')
    username=models.CharField(max_length=500,verbose_name='昵称')
    content=models.CharField(max_length=1000,verbose_name='电影评论')
    createtime=models.CharField(auto_now_add=True,verbose_name='创建时间')
    class Meta:
        db_table='comment'
