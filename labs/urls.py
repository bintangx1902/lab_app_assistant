"""labs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/clearcache/', include('clearcache.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('robots.txt', include('robots.urls')),
    path('static/<path>', serve, settings.STATIC_ROOT),
    path('media/<path>', serve, settings.MEDIA_ROOT),
]

urlpatterns += [
    path('file/', include('file_control.urls', namespace='file')),
    path('assistant/', include('assistant.urls', namespace='assist')),
    path('api/', include('api.urls', namespace='api')),
    path('', include('presence.urls', namespace='presence')),
]

if not settings.DEBUG or settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

