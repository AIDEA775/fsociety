from django.conf.urls import url

from . import views

app_name = 'video'
urlpatterns = [
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^delete/$', views.delete, name='delete'),
]
