from django.conf.urls import url

from user import views

urlpatterns = [
    url('^/register$', views.register),
    # url('^/login$', views.login),
    url(r'^information$',views.information),
]
