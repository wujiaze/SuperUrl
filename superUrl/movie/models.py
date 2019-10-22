from django.db import models

# Create your models here.

class MovieInfomation(models.Model):
    name=models.CharField(max_length=500,verbose_name='电影名',null=False)
    director=models.CharField(max_length=100,verbose_name='导演',default='')
    actor=models.CharField(max_length=1000,verbose_name='演员',default='')
    releasetime=models.DateTimeField(default='')
    download_count=models.IntegerField(default=0,verbose_name='下载量')
    star_one=models.IntegerField(default=0,verbose_name='一星数')
    star_two = models.IntegerField(default=0, verbose_name='二星数')
    star_three = models.IntegerField(default=0, verbose_name='三星数')
    star_four = models.IntegerField(default=0, verbose_name='四星数')
    star_five = models.IntegerField(default=0, verbose_name='五星数')
    star_avg = models.FloatField(default=0, verbose_name='平均星数')
    create_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time=models.DateTimeField(auto_now=True,verbose_name='更新时间')
    url=models.CharField(max_length=1000,verbose_name='电影资源链接')

    class Meta:
        db_table='movie_information'



class MovieKeyword(models.Model):
    keyword=models.CharField(max_length=200,verbose_name='关键字',unique=True,null=False)
    create_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    movieInfomation=models.ManyToManyField(MovieInfomation)

    class Meta:
        db_table='movie_keyword'
