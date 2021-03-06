from django.conf import settings
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin

from ticketing import views as tviews

from Post import views as pv
from restapi import views
from rest_framework import routers
from rest_framework.authtoken import views as v

from push_notifications.api.rest_framework import APNSDeviceViewSet, GCMDeviceViewSet
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = routers.DefaultRouter()
router.register(r'events', views.PostViewSet)

router.register(r'music', views.MusicViewSet, 'music')
router.register(r'performing_arts', views.PerformingArtsViewSet, 'performing_arts')
router.register(r'art', views.ArtViewSet, 'art')
router.register(r'sports', views.SportsViewSet, 'sports')
router.register(r'charity', views.CharityViewSet, 'charity')
router.register(r'comedy', views.ComedyViewSet, 'comedy')
router.register(r'poetry', views.PoetryViewSet, 'poetry')
router.register(r'think', views.ThinkViewSet, 'think')
router.register(r'wpoppin', views.WpoppinViewSet, 'wpoppin')
router.register(r'events_today', views.PostTodayViewSet, 'events_today')
router.register(r'events_tomorrow', views.PostTomorrowViewSet, 'events_tomorrow')
router.register(r'events_this_week', views.PostThisWeekViewSet, 'events_this_week')
router.register(r'accounts', views.AccountViewSet)
router.register(r'events_this_month', views.PostThisMonthViewSet, 'events_this_month')

#router.register(r'token-auth', views.CustomObtainAuthToken, 'token-auth')

router.register(r'blog', views.BlogViewSet, 'blog')

router.register(r'organizations', views.OrganizationsViewSet, 'organizations')
router.register(r'account', views.AccountViewSet, 'accounts')
router.register(r'myaccount', views.MyAccountViewSet, 'myaccounts')
#router.register(r'users', views.UserViewSet, 'users')
router.register(r'myfeed', views.FeedViewSet, 'myfeed')
router.register(r'filteredevents', views.FilteredEventViewSet, 'filteredevents')
router.register(r'myrecommended', views.MyRecommendedViewSet, 'myrecommended')
router.register(r'notificationfeed', views.NotificationFeedViewSet, 'notificationfeed')

#notifications
router.register(r'device/apns', APNSDeviceViewSet)
router.register(r'device/gcm', GCMDeviceViewSet)
router.register(r'devices', FCMDeviceAuthorizedViewSet)



urlpatterns = [
    url(r"^$", pv.survey, name="home"),
    url(r"^restricted/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^account/social/accounts/$", TemplateView.as_view(template_name="account/social.html"), name="account_social_accounts"),
    url(r"^account/social/", include("social.apps.django_app.urls", namespace="social")),
    url(r"^post/", include('Post.urls')),
    url(r"^stories/", include('blog.urls')),
    url(r"^search/", include('haystack.urls')),
    #url(r'^comments/', include('django_comments.urls')),
    url(r'^messages/', include("pinax.messages.urls", namespace="pinax_messages")),

    #api endpoints and oauth2
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/wp/auth/', include('djoser.urls')), #use for wpoppin registration with email/username/password

    #only returned the token: returns token and user id
    url(r'^api-token-auth/', v.obtain_auth_token), #Convert Username and Password to What'sPoppin Token

    #being currently used
    url(r'^token-auth/', views.CustomObtainAuthToken.as_view()),  #Convert Username and Password to What'sPoppin Token and id

    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')), #our oath2 app

    url(r'^api/auth/', include('rest_framework_social_oauth2.urls')),  #convert_token facebook to What'sPoppin Token

    #url(r"^profile/", include("activity_stream.urls")),

    #different homepages
    url(r"^sports$", TemplateView.as_view(template_name="sports_homepage.html"), name="sports_home"),
    url(r"^music", TemplateView.as_view(template_name="music_homepage.html"), name="music_home"),
    url(r"^arts", TemplateView.as_view(template_name="performing_arts_homepage.html"), name="performing_arts_home"),
    url(r"^academics", TemplateView.as_view(template_name="academics_homepage.html"), name="academics_home"),
    url(r"^joinourteam", TemplateView.as_view(template_name="join.html"), name="join"),
    url(r"^privacy", TemplateView.as_view(template_name="privacy.html"), name="privacy"),
    url(r"^about", TemplateView.as_view(template_name="about.html"), name="about"),
    url(r"^storieswriter", TemplateView.as_view(template_name="stories-writer.html"), name="storieswriter"),
    url(r"^marketingintern", TemplateView.as_view(template_name="marketing-intern.html"), name="marketingintern"),

    #ticketing
    url(r'^api/confirm_ticket/$', views.confirm_ticket),
    url(r'^api/generate_confirmation/$', views.generate_confirmation),
    url(r'^api/resend_confirmation/$', views.resend_confirmation),
    url(r'^purchase/(?P<event_id>\d+)/$', tviews.purchase),
    url(r'^checkout/$', tviews.checkout)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
