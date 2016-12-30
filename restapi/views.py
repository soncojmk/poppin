from django.shortcuts import render


# Create your views here.


#REST API
from Post.serializers import PostSerializer
from rest_framework import generics
from Post.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from Post.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework import status
from Post.models import Post
from django.db.models import Q

from datetime import date, timedelta

'''
# API authentication
from social.apps.django_app.utils import strategy
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import parsers
from rest_framework.authentication import get_authorization_header
from rest_framework.authtoken.serializers import AuthTokenSerializer


@strategy()
def register_by_access_token(request, backend):
    backend = request.strategy.backend
    # Split by spaces and get the array
    auth = get_authorization_header(request).split()

    if not auth or auth[0].lower() != b'token':
        msg = 'No token header provided.'
        return msg

    if len(auth) == 1:
        msg = 'Invalid token header. No credentials provided.'
        return msg

    access_token = auth[1]

    user = backend.do_auth(access_token)

    return user


# Pour une vraie integration au rest framework
class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    model = Token

    # Accepte un backend en parametre : 'auth' pour un login / pass classique
    def post(self, request, backend):
        serializer = self.serializer_class(data=request.DATA)

        if backend == 'auth':
            if serializer.is_valid():
                token, created = Token.objects.get_or_create(user=serializer.object['user'])
                return Response({'token': token.key})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            user = register_by_access_token(request, backend)

            if user and user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'id': user.id, 'name': user.username, 'firstname': user.first_name, 'userRole': 'user', 'token': token.key})


class ObtainUser(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    model = Token

    # Renvoi le user si le token est valide
    def get(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if request.META.get('HTTP_AUTHORIZATION'):

            auth = request.META.get('HTTP_AUTHORIZATION').split()

            if not auth or auth[0].lower() != b'token' or len(auth) != 2:
                msg = 'Invalid token header. No credentials provided.'
                return Response(msg, status=status.HTTP_401_UNAUTHORIZED)

            token = Token.objects.get(key=auth[1])
            if token and token.user.is_active:
                return Response({'id': token.user_id, 'name': token.user.username, 'firstname': token.user.first_name, 'userRole': 'user', 'token': token.key})
        else:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class ObtainLogout(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    model = Token

    # Logout le user
    def get(self, request):
        return Response({'User': ''})
'''




#REST API VIEWSETS
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostTodayViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.filter(date=date.today()).order_by('time')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)


class PostTomorrowViewSet(viewsets.ModelViewSet):

    today = date.today()
    startdate = today + timedelta(days=1)
    enddate = startdate + timedelta(days=2)

    queryset = Post.objects.filter(date__range=[startdate, enddate]).order_by('-posted_date')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)


class PostThisWeekViewSet(viewsets.ModelViewSet):

    startdate = date.today()
    enddate = startdate + timedelta(days=6)

    queryset = Post.objects.filter(date__range=[startdate, enddate]).order_by('-posted_date')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

class PostThisMonthViewSet(viewsets.ModelViewSet):

    startdate = date.today()
    enddate = startdate + timedelta(days=30)

    queryset = Post.objects.filter(date__range=[startdate, enddate]).order_by('-posted_date')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)


class MusicViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.filter(category = Post.MUSIC).order_by('-posted_date')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SportsViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.filter(category = Post.SPORTS).order_by('-posted_date')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CharityViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.filter(category = Post.FUNDRAISERS).order_by('-posted_date')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PerformingArtsViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.filter(Q(category = Post.DANCE) | Q(category=Post.PERFORMING_ARTS) | Q(category = Post.THEATRE)).order_by('-posted_date')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ComedyViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.filter(category = Post.COMEDY).order_by('-posted_date')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PoetryViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.filter(category = Post.POETRY).order_by('-posted_date')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArtViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.filter(category = Post.ART).order_by('-posted_date')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ThinkViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.filter(Q(category = Post.LECTURE) | Q(category=Post.ACADEMIC) | Q(category = Post.DEBATE) | Q(category = Post.PROFESSIONAL) | Q(category = Post.CLUB_EVENT)).order_by('-posted_date')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class WpoppinViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.filter(category = Post.WP).order_by('-posted_date')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)





