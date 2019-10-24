from django.db import models
from user.models import UserProfile
# Create your models here.


class history(models.Model):
    keyword = models.CharField(max_length=20,verbose_name='查询关键字')
    create_time = models.DateTimeField(auto_now_add=True)

    userprofile = models.ForeignKey(UserProfile)

    class Meta:
        db_table = 'history'