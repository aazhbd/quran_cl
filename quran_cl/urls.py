
from django.conf.urls import url
from django.contrib import admin

from django.views.generic import TemplateView

from quran import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='index'),
    url(r'^home$', views.HomeView.as_view(), name='index'),
    url(r'^info$', views.viewInfo, name='info'),

    url(r'^login$', views.viewLogin, name='login'),
    url(r'^logout$', views.viewLogout, name='logout'),
    url(r'^signup$', views.viewSignup, name='signup'),
    url(r'^discuss$', views.viewDiscuss, name='discuss'),

    url(r'^(?P<chap>\d+)/?$', views.viewChapter, name='chapter'),
    url(r'^getchapter$', views.getChapter, name='getchapter'),

    url(r'^(?P<chap>\d+)/(?P<verse>\d+)/?$', views.viewVerse, name='verse'),
    url(r'^getverse$', views.getVerse, name='getverse'),

    url(r'^search/(?P<search>.+?)/(?P<page>\d+)/?$', views.viewSearch, name='search'),
    url(r'^search/(?P<search>.+?)/?$', views.viewSearch, name='search'),
    url(r'^search/?$', views.viewSearch, name='search'),

    url(r'^google37851790136c6f53.html/$', TemplateView.as_view(template_name='google37851790136c6f53.html'), name='google-search-console'),
    
    url(r'^robots\.txt$', 'django.shortcuts.render', kwargs={
        'template_name': 'robots.txt',
        'content_type': 'text/plain',
    }),
    
    url(r'^admin/', admin.site.urls),
]
