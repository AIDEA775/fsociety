from django.conf.urls import url

from . import views

app_name = 'video'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^uploaded/$', views.uploaded, name='uploaded'),
    url(r'^uploaded/delete/$', views.delete, name='delete'),
    url(r'^watched/$', views.watched, name='watched'),
    url(r'^friends_videos/$', views.friends_videos, name='friends_videos'),
    url(r'^feed/$', views.feed, name='feed'),
    url(r'^(?P<video_id>[0-9]+)/$', views.player, name='player'),
]
