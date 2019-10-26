from django.conf.urls import url
from rank_keylist import views


urlpatterns = [
    url('^/rank$',views.get_rank),
    url('^/keylist$',views.get_keylist)
]