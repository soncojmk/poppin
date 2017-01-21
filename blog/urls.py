from django.conf.urls import url, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', views.blog_list, name='blog_list'),
    url(r'^post/(?P<pk>\d+)/$', views.blog_detail, name='blog_detail'),
    url(r'^post/new/$', views.blog_new, name='blog_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.blog_edit, name='blog_edit'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.blog_remove, name='blog_remove'),

]