from django.conf.urls import patterns, include, url
from . import views

urlpatterns = [
    url(r'^like/(?P<pk>\d+)/$', views.LikeToggleView, name="user_objects_liked"),
    
]

