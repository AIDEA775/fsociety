from django.conf.urls import url
from . import views

app_name = 'video'
urlpatterns = [
    url(r'^list/$', views.list, name='list'),
    url(r'^my_videos/$', views.my_videos, name='my_videos'),
    url(r'^my_videos/delete$', views.video_delete, name='video_delete'),
]
