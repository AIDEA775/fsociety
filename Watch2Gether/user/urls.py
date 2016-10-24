from django.conf.urls import url

from . import views

app_name = 'user'
urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^friends/$', views.friends, name='friends'),
    url(r'^requests/accept$', views.request_accept, name='request_accept'),
    url(r'^requests/reject$', views.request_reject, name='request_reject'),
    url(r'^requests/send$', views.request_send, name='request_send'),
    url(r'^list/$', views.list, name='list'),
]
