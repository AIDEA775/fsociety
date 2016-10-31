from django.conf.urls import url
from . import views

app_name = 'video'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^my_videos/$', views.my_videos, name='my_videos'),
    url(r'^my_videos/delete/$', views.delete, name='delete'),
    url(r'^friends_videos/$', views.friends_videos, name='friends_videos'),
    url(r'^feed/$', views.feed, name='feed'),
    url(r'^player/(?P<video_id>[0-9]+)/$', views.player, name='player'),
]
