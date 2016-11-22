"""VinVC URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^', include('login.urls')),
    url(r'^user/', include('user.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^video/', include('video.urls')),
    url(r'^friendship/', include('friendship.urls')),
    url(r'^', include('video_room.urls')),

    url(r'^admin/', admin.site.urls),

    # Python Social Auth URLs
    url('', include('social.apps.django_app.urls', namespace='social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
