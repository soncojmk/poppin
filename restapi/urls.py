from Post.views import PostViewSet, UserViewSet, api_root
from rest_framework import renderers

post_list = PostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
post_detail = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})


urlpatterns = format_suffix_patterns([
    url(r'^$', api_root),
    url(r'^events/$', post_list, name='post-list'),
    url(r'^events/(?P<pk>[0-9]+)/$', post_detail, name='post-detail'),
    url(r'^events/(?P<pk>[0-9]+)/highlight/$', post_highlight, name='post-highlight'),
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail')
])