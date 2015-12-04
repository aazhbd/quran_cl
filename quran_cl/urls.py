
from django.conf.urls import url
from django.contrib import admin

from quran import views

urlpatterns = [
    url(r'^$', views.viewHome, name='index'),
    url(r'^home$', views.viewHome, name='index'),
    url(r'^info$', views.viewInfo, name='info'),

    url(r'^login$', views.viewLogin, name='login'),
    url(r'^discuss$', views.viewDiscuss, name='discuss'),
    url(r'^logout$', views.viewLogout, name='discuss'),

    url(r'^admin/', admin.site.urls),
]
