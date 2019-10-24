from django.conf.urls import url

from music import views

urlpatterns = [
    url('^$',views.search_music),
    url('^/keylist$',views.get_keylist),
    url('^/rank$',views.get_rank),
    url('^/history$',views.get_history),
    url('^/download$',views.add_download)
]