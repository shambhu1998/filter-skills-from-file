from django.conf.urls import url

from file import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
]
