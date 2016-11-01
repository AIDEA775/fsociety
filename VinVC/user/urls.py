from django.conf.urls import url

from . import views

app_name = 'user'
urlpatterns = [
    url(r'^(?P<user_id>[0-9]+)/$', views.profile, name='profile'),
    url(r'^friends/(?P<user_id>[0-9]+)/$', views.friends, name='friends'),
    url(r'^requests/$', views.requests, name='requests'),
    url(r'^requests/accept$', views.request_accept, name='request_accept'),
    url(r'^requests/reject$', views.request_reject, name='request_reject'),
    url(r'^requests/send$', views.request_send, name='request_send'),
    url(r'^requests/api$', views.requests_api, name='requests_api'),
    url(r'^list/$', views.list, name='list'),
]
