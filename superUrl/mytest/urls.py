from django.conf.urls import url

from mytest import views

urlpatterns = [
    url(r'^/(?P<keyword>.*)$', views.pushMysql)
]
