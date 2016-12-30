from Post.views import PostViewSet, UserViewSet, MusicViewSet, SportsViewSet, CharityViewSet, PostTodayViewSet, PostTomorrowViewSet, PostThisWeekViewSet, PostThisMonthViewSet, api_root
from rest_framework import renderers
#from .views import ObtainAuthToken

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


music = MusicViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
music_detail = MusicViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

sports = SportsViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
sports_detail = SportsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


charity = CharityViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
charity_detail = CharityViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


events_today = PostTodayViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

events_tomorrow = PostTomorrowViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

events_this_week = PostThisWeekViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

events_this_month = PostThisMonthViewSet.as_view({
    'get': 'list',
    'post': 'create'
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

    url(r'^music/$', music, name='music'),
    url(r'^music/(?P<pk>[0-9]+)/$', music_detail, name='music_detail'),

    url(r'^sports/$', sports, name='sports'),
    url(r'^sports/(?P<pk>[0-9]+)/$', sports_detail, name='sports-detail'),

    url(r'^charity/$', charity, name='charity'),
    url(r'^charity/(?P<pk>[0-9]+)/$', charity_detail, name='charity-detail'),

    url(r'^events_today/$', events_today, name='events_today'),
    url(r'^events_tomorrow/$', events_tomorrow, name='events_tomorrow'),
    url(r'^events_this_week/$', events_this_week, name='events_this_week'),
    url(r'^events_this_month/$', events_this_month, name='events_this_month'),


    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),

    #url(r'^api-token/login/(?P[^/]+)/$', ObtainAuthToken.as_view(), name='token'),
])