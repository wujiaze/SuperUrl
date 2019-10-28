from django.db import models

# Create your models here.


class PictureInformation(models.Model):
    describe = models.CharField(max_length=200,default='好美的图',verbose_name='图片描述')
    download_count = models.IntegerField(default=0,verbose_name='下载量')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    url = models.CharField(max_length=1000,null=False,verbose_name='图片资源链接')


    class Meta:
        db_table = 'picture_information'




class PictureKeyword(models.Model):
    keyword = models.CharField(max_length=50,null=False,unique=True,verbose_name='关键字')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    musicinformation = models.ManyToManyField(PictureInformation)

    class Meta:
        db_table = 'picture_keyword'






