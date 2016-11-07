from django.conf.urls import url

from . import views

app_name = 'user'
urlpatterns = [
    url(r'^(?P<user_id>[0-9]+)/$', views.profile, name='profile'),
    url(r'^(?P<user_id>[0-9]+)/friends/$', views.friends, name='friends'),
    url(r'^(?P<user_id>[0-9]+)/uploaded/$', views.uploaded, name='uploaded'),
    url(r'^(?P<user_id>[0-9]+)/watched/$', views.watched, name='watched'),
    url(r'^requests/$', views.requests, name='requests'),
    url(r'^requests/api$', views.requests_api, name='requests_api'),
]
