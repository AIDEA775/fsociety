from django.conf.urls import url
from . import views

app_name = 'video_room'
urlpatterns = [
    url(r'^(?P<video_id>[0-9]+)/(?P<chat_room>[0-9]+)/$', views.player, name='player'),
]
