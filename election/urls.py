"""
URL configuration for election project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
import requests
from django.contrib import admin
from django.urls import path,include
from django.urls import path
from candidato.models import Publishing
from django.conf.urls.static import static
from election import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

if not Publishing.objects.first():
    Publishing.objects.create()


import re

def data(self):
    url = self.request.build_absolute_uri()
    pattern = "^https:\/\/[0-9A-z.]+.[0-9A-z.]+.[a-z]+$"
    result = re.match(pattern, url)

    if result:
        print(result)
    else:
        print("Invalid URL")

data()

urlpatterns = [
    path("", include('candidato.urls')),
    path("auths/", include("auths.urls")),
    path('voterlive/', include('voter.urls')),
    path('auttlogin/',include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),


]
if settings.DEBUG:  # new
    urlpatterns += static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
    urlpatterns += staticfiles_urlpatterns()


