from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib.auth.views import logout
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^login$', views.login, name='login'),
    url(r'^signup$', views.signup, name='signup'),

    # Python Social Auth URLs
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^logout/$', logout, {'next_page': '/'}, name='user-logout'),
]
