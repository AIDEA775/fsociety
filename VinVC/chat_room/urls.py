from django.conf.urls import url

from . import views

app_name = 'chat_room'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^login/$',views.login,name='login'),
    # url(r'^logout/$',views.logout,name='logout'),
    url(r'^api/$',views.chat_api,name='chat_api'),
    url(r'^api/users/$',views.logged_chat_users,name='logged_chat_users'),
    url(r'^api/users/update/$',views.update_time,name='update_time'),
]
