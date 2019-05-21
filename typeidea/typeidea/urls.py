"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from typeidea.views import hello,current_time,hours_ahead,current_datetime,ua_dispaly,display_meta,contact
from books import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/$',hello),
    url(r'^current_time/$',current_time),
    url(r'^current_datetime$',current_datetime),
    url(r'^time/plus/(\d{1,2})/$',hours_ahead),
    url(r'^ua_display/$',ua_dispaly),
    url(r'^display_meta/$',display_meta),
    url(r'^search-form/$',views.search_form),
    url(r'^search',views.search),
    url(r'^contact/$',contact),
]
