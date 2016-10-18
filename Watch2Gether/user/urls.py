from django.conf.urls import url

from . import views

app_name = 'user'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^friends/$', views.friends, name='friends'),
]
