from Post.views import NotificationFeedViewSet, PostViewSet, OrganizationsViewSet, MyRecommendedViewSet, FilteredEventViewSet, UserViewSet, FeedViewSet, MusicViewSet, MyAccountViewSet, AccountViewSet, SportsViewSet, CharityViewSet, PostTodayViewSet, PostTomorrowViewSet, PostThisWeekViewSet, PostThisMonthViewSet, api_root
from rest_framework import renderers
from blog.views import BlogViewSet
from .views import CustomObtainAuthToken


#from .views import ObtainAuthToken

blog_list = BlogViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
blog_detail = BlogViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


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


'''
user_list = UserViewSet.as_view({
    'post': 'create'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})
'''

organizations_list = OrganizationsViewSet.as_view({
    'get': 'list',
    'post': 'create'

})


account_list = AccountViewSet.as_view({
    'post': 'create'
})
account_detail = AccountViewSet.as_view({
    'get': 'retrieve'
})


myaccount_list = MyAccountViewSet.as_view({
    'post': 'create'
})
myaccount_detail = MyAccountViewSet.as_view({
    'get': 'retrieve'
})


myrecommended_list = MyRecommendedViewSet.as_view({
    'post': 'create'
})
myrecommended_detail = MyRecommendedViewSet.as_view({
    'get': 'retrieve'
})


feed_list = FeedViewSet.as_view({
    'post': 'create'
})
feed_detail = FeedViewSet.as_view({
    'get': 'retrieve'
})


filteredevent_list = FilteredEventViewSet.as_view({
    'post': 'create',
    'get': 'list'
})
filteredevent_detail = FilteredEventViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


notificationfeed_list = NotificationFeedViewSet.as_view({
    'post': 'create',
    'get': 'list'
})
notificationfeed_detail = NotificationFeedViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
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


    #url(r'^users/$', user_list, name='user-list'),
    #url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),

    url(r'^organizations/$', organizations_list, name='organizations-list'),
    url(r'^accounts/(?P<pk>[0-9]+)/$', account_detail, name='organizations-detail'),

    url(r'^accounts/$', account_list, name='user-list'),
    url(r'^accounts/(?P<pk>[0-9]+)/$', account_detail, name='user-detail'),

    url(r'^myaccount/$', myaccount_list, name='account-list'),
    url(r'^accounts/(?P<pk>[0-9]+)/$', myaccount_detail, name='account-detail'),

    url(r'^myaccount/$', myrecommended_list, name='account-list'),
    url(r'^accounts/(?P<pk>[0-9]+)/$', myrecommended_detail, name='account-detail'),

    url(r'^myfeed/$', feed_list, name='feed-list'),
    url(r'^myfeed/(?P<pk>[0-9]+)/$', feed_detail, name='feed-detail'),

    url(r'^filteredevent/$', filteredevent_list, name='post-list'),
    url(r'^filteredevent/(?P<pk>[0-9]+)/$', filteredevent_detail, name='post-detail'),

    url(r'^notificationfeed/$', notificationfeed_list, name='notification-list'),
    url(r'^notificationfeed/(?P<pk>[0-9]+)/$', notificationfeed_detail, name='notification-detail'),

    #url(r'^api-token/login/(?P[^/]+)/$', ObtainAuthToken.as_view(), name='token'),
    #url(r'^token-auth/', CustomObtainAuthToken.as_view()),

    url(r'^blog/$', blog_list, name='blog_list'),
    url(r'^blog/(?P<pk>[0-9]+)/$', blog_detail, name='blog-detail'),

])
