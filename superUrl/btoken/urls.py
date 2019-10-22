from django.conf.urls import url

from btoken import views

urlpatterns = [
    url(r'^$', views.tokens)
]
