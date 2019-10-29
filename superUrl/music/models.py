from django.db import models

# Create your models here.


class MusicInformation(models.Model):
    name = models.CharField(max_length=100,null=False,verbose_name='音乐名')
    star = models.CharField(max_length=500,null=False,default='佚名',verbose_name='歌手')
    download_count = models.IntegerField(default=0,verbose_name='下载量')
    time = models.CharField(max_length=20,default='未知',verbose_name='时长')
    star_one = models.IntegerField(default=0,verbose_name='一星数')
    star_two = models.IntegerField(default=0,verbose_name='二星数')
    star_three = models.IntegerField(default=0,verbose_name='三星数')
    star_four = models.IntegerField(default=0,verbose_name='四星数')
    star_five = models.IntegerField(default=0,verbose_name='五星数')
    star_avg = models.FloatField(default=0,verbose_name='平均星数')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    url = models.CharField(max_length=1000,null=False,verbose_name='音乐资源链接')

    class Meta:
        db_table = 'music_information'




class MusicKeyword(models.Model):
    keyword = models.CharField(max_length=50,null=False,unique=True,verbose_name='关键字')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    musicinformation = models.ManyToManyField(MusicInformation)

    class Meta:
        db_table = 'music_keyword'






