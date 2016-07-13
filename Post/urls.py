from django.conf.urls import url, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^search/?$', views.MySearchView, name='search_view'),
    url(r"^likes/", include("pinax.likes.urls", namespace="pinax_likes")),
    url(r'^tag/$', views.categories, name='categories'),

    #url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    #url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),

    url(r'^eventcomment/(?P<pk>\d+)/remove/$', views.event_comment_remove, name='event_comment_remove'),
    url(r'^questioncomment/(?P<pk>\d+)/remove/$', views.question_comment_remove, name='question_comment_remove'),
    #url(r'^category$', views.category_list, name='category_list'),
    #url(r'^category/(?P<pk>\d+)/$', views.category_detail, name='category_detail'),
    
    url(r'^question/$', views.question_list, name='question_list'),
    url(r'^question/(?P<pk>\d+)/$', views.question_detail, name='question_detail'),
    url(r'^question/new/$', views.question_new, name='question_new'),
    url(r'^question/(?P<pk>\d+)/edit/$', views.question_edit, name='question_edit'),
    url(r'^question/(?P<pk>\d+)/remove/$', views.question_remove, name='question_remove'),
    url(r"^post/question/$", TemplateView.as_view(template_name="Post/post.html"), name="post"),

    url(r"^myprofile/about/(?P<pk>\d+)/$", views.my_profile, name='my_profile'),
    url(r"^myprofile/myevents/$", views.my_events, name='my_events'),
    url(r"^myprofile/myquestions/$", views.my_questions, name='my_questions'),
    url(r"^feed/$", views.feed, name='feed'),
    url(r'^myprofile/new/$', views.ProfileObjectMixin, name='profile_new'),
    #url(r'^myprofile/(?P<pk>\d+)/edit/$', views.profile_edit, name='profile_edit'),



]


