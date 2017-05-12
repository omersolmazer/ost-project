"""ost-reservation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/{{ docs_version }}/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^/', views.index, name='index'),
    url(r'^reservation/', views.reservation, name='reservation'),
    url(r'^resources', views.resources, name='resources'),
    url(r'^resource/(?P<resource_id>[0-9]+)/$', views.resource, name='resource'),

    url(r'^index/', views.index, name='index'),
    url(r'^logout', views.user_logout, name='logout'),
    url(r'^login', views.user_login, name='login'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^users/$', views.users, name='users'),
    url(r'^404/$', views.err, name='err'),
    url(r'^admin/', admin.site.urls),
]
