"""Watch2Gether URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.index, name='index')
Class-based views
    1. Add an import:  from other_app.views import Index
    2. Add a URL to urlpatterns:  url(r'^$', Index.as_view(), name='index')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('videochat.urls')),
    url(r'^user/', include('user.urls')),
    url(r'^admin/', admin.site.urls),
]
