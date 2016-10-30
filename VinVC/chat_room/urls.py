from django.conf.urls import include, url
from . import views

app_name='login'
urlpatterns = [
    url(r'^(?P<video_id>[0-9]+)/$', views.index, name='index'),
    url(r'^(?P<video_id>[0-9]+)/api/$', views.api, name='api'),
]
