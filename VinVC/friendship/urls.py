from django.conf.urls import url

from . import views

app_name = 'friendship'
urlpatterns = [
    url(r'^requests/api$', views.requests_api, name='requests_api'),
]
