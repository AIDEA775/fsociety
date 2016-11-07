from django.conf.urls import url

from . import views

app_name = 'video'
urlpatterns = [
    url(r'^feed/$', views.feed, name='feed'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^(?P<video_id>[0-9]+)/$', views.player, name='player'),
]
