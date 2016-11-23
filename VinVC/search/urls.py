from django.conf.urls import url

from . import views

app_name = 'search'
urlpatterns = [
    url(r'^$', views.search, name='search'),
    url(r'^api/$', views.get_videos, name='get_videos')
]
