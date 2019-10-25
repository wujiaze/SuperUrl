from django.conf.urls import url

from history import views


urlpatterns = [
    url(r'^/history$',views.get_history)
]