from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views

app_name = 'login'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
]
