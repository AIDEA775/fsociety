from django.conf.urls import url

from . import views

app_name = 'user'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^friends/$', views.friends, name='friends'),
    url(r'^requests/accept$', views.friendship_accept, name='friendship_accept'),
    url(r'^requests/reject$', views.friendship_reject, name='friendship_reject'),
]
