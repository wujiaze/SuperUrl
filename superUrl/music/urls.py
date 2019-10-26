from django.conf.urls import url

from music import views

urlpatterns = [
    url('^$',views.search_music),
]