from django.db import models

# Create your models here.


class Finger(models.Model):
    url = models.CharField(max_length=32,verbose_name='url指纹')
    is_active = models.BooleanField(default=True,verbose_name='是否可用')


    class Meta:
        db_table = 'finger'


