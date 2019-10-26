from django.conf.urls import url

from history import views


urlpatterns = [
    url(r'^$',views.get_history)
]