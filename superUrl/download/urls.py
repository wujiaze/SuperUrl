from django.conf.urls import url
from download import views


urlpatterns = [
    url('^$',views.add_download)
]