from django.db import models


# Create your models here.

class UserProfile(models.Model):
    phonenumber = models.CharField('手机号', max_length=11, unique=True)
    nickname = models.CharField('昵称', max_length=30, null=False)
    password = models.CharField('密码', max_length=32, null=False)
    avatar = models.ImageField(upload_to='avatar', null=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_ime = models.DateTimeField('更新时间', auto_now=True)
    login_time = models.DateTimeField('登录时间', null=True)

    # email = models.EmailField('邮箱')
    # login_time = models.DateTimeField('登录时间', )
    # lock_score = models.IntegerField('分布式锁测试字段', default=0, null=True)
    # ll = models.IntegerField('分布式锁测试字段', default=0, null=False)

    class Meta:
        db_table = 'user_profile'
