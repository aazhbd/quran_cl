
from django.conf.urls import url
from django.contrib import admin

from quran import views

urlpatterns = [
    url(r'^$', views.viewHome, name='index'),
    url(r'^home$', views.viewHome, name='index'),
    url(r'^info$', views.viewInfo, name='info'),

    url(r'^login$', views.viewLogin, name='login'),
    url(r'^logout$', views.viewLogout, name='logout'),
    url(r'^signup$', views.viewSignup, name='signup'),
    url(r'^discuss$', views.viewDiscuss, name='discuss'),

    url(r'^(?P<chap>\d+)/?$', views.viewChapter, name='chapter'),
    url(r'^getchapter$', views.getChapter, name='getchapter'),

    url(r'^(?P<chap>\d+)/(?P<verse>\d+)/?$', views.viewVerse, name='verse'),
    url(r'^getverse$', views.getVerse, name='getverse'),

    url(r'^admin/', admin.site.urls),
]
