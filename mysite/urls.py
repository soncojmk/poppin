from django.conf import settings
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin

from Post import views as pv
from restapi import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'events', views.PostViewSet)
router.register(r'users', views.UserViewSet)




urlpatterns = [
    url(r"^$", pv.survey, name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^account/social/accounts/$", TemplateView.as_view(template_name="account/social.html"), name="account_social_accounts"),
    url(r"^account/social/", include("social.apps.django_app.urls", namespace="social")),
    url(r"^post/", include('Post.urls')),
    url(r"^search/", include('haystack.urls')),
    #url(r'^comments/', include('django_comments.urls')),
    url(r'^messages/', include("pinax.messages.urls", namespace="pinax_messages")),

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r"^profile/", include("activity_stream.urls")),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
