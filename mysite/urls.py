from django.conf import settings
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin

from Post import views as pv
from restapi import views
from rest_framework import routers
from rest_framework.authtoken import views as v

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
router.register(r'accounts', views.UserViewSet)
router.register(r'events_this_month', views.PostThisMonthViewSet, 'events_this_month')

router.register(r'blog', views.BlogViewSet, 'blog')


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
    url(r'^api-token-auth/', v.obtain_auth_token), #Convert Username and Password to What'sPoppin Token
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')), #our oath2 app

    url(r'^api/auth/', include('rest_framework_social_oauth2.urls')),  #convert_token facebook to What'sPoppin Token

    url(r"^profile/", include("activity_stream.urls")),

    #different homepages
    url(r"^sports$", TemplateView.as_view(template_name="sports_homepage.html"), name="sports_home"),
    url(r"^music", TemplateView.as_view(template_name="music_homepage.html"), name="music_home"),
    url(r"^arts", TemplateView.as_view(template_name="performing_arts_homepage.html"), name="performing_arts_home"),
    url(r"^academics", TemplateView.as_view(template_name="academics_homepage.html"), name="academics_home"),
    url(r"^joinourteam", TemplateView.as_view(template_name="join.html"), name="join"),
    url(r"^privacy", TemplateView.as_view(template_name="privacy.html"), name="privacy"),



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
