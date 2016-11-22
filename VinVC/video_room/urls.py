from django.conf.urls import url
from . import views

app_name = 'video_room'
urlpatterns = [
    url(r'^feed/$', views.feed, name='feed'),
    url(r'^room/(?P<video_id>[0-9]+)/(?P<room_id>[0-9]+)/$', views.join, name='join'),
    url(r'^room/(?P<video_id>[0-9]+)/$', views.new, name='new'),
]
