from django.shortcuts import render


# Create your views here.


#REST API
from Post.serializers import PostSerializer, EventSerializer, CommentSerializer, CreateCommentSerializer
from blog.serializers import BlogSerializer
from notifications.serializers import NotificationSerializer
from notifications.models import Notification
from rest_framework import generics
from Post.serializers import UserSerializer
from account.serializers import AccountSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from Post.permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnlyAccount
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework import status
from Post.models import Post, EventComment
from account.models import Account
from blog.models import Blog
from django.db.models import Q
from rest_framework.permissions import AllowAny
from django.utils import timezone
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework import filters

from Post.permissions import IsStaffOrTargetUser

from datetime import date, timedelta
from rest_framework.generics import CreateAPIView
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.db.models import Count
from fcm_django.models import FCMDevice

from rest_framework.decorators import api_view
from .ticket_confirmation import TicketConfirmation
from django.http import HttpResponse
from django.http import JsonResponse
import json
from notifications.signals import notify


@api_view(['POST'])
def confirm_ticket(request, pk=None):
    ticketing = TicketConfirmation()
    try:
        data = request.data.dict()
        body = json.loads(data['_content'])
        confirmation_num = body['confirmation_num']
        response = {'status': ticketing.confirm(confirmation_num)}
        return JsonResponse(response)
    except:
        return JsonResponse({'status':'error'})

@api_view(['POST'])
def generate_confirmation(request, pk=None):
    try:
        data = request.data.dict()
        body = json.loads(data['_content'])
        to_email = body['email']
        event_name = body['event_name']
        user_id = body['user_id']
        username = body['username']
        ticketing = TicketConfirmation()
        response = {'confirmation_num':ticketing.generate_confirmation(to_email, event_name, user_id, username)}
        return JsonResponse(response)
    except:
        return JsonResponse({'confirmation_num':'error'})

@api_view(['POST'])
def resend_confirmation(request, pk=None):
    try:
        data = request.data.dict()
        body = json.loads(data['_content'])
        to_email = body['email']
        user_id = body['user_id']
        username = body['username']
        event_name = body['event_name']
        ticketing = TicketConfirmation()
        response = {'confirmation_num':ticketing.resend_confirmation(to_email, event_name, user_id, username)}
        return JsonResponse(response)
    except:
        return JsonResponse({'confirmation_num':'error'})

#Overiding api-token-auth to get id along with the default response
class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


#REST API VIEWSETS

'''wpoppin viewsets'''
class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class =  UserSerializer
    model = User

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST'
                else IsStaffOrTargetUser()),


class BlogViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class NotificationFeedViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        return self.request.user.notifications.unread()

    def perform_create(self, serializer):
        serializer.save(actor=self.request.user)




#don't forget to change the serializer to EventSerializer when you update so that you can allow people to see the details of old events
class PostViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """

    startdate = date.today()
    enddate = startdate + timedelta(days=365)

    queryset = Post.objects.filter(date__range=[startdate, enddate]).order_by('-posted_date')
    now = timezone.localtime(timezone.now())
    #queryset = Post.objects.filter(posted_date__lte=timezone.now()).filter(Q(date__gte=now.date())).order_by('-posted_date')
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, JSONParser)

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    model = Post

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    #add a comment to an event
    @detail_route(methods=['get', 'post', 'delete'])
    def post_comment(self, *args, **kwargs):
        comment = kwargs.pop('comment', None)
        pk = kwargs.pop('pk', None)
        request = self.request
        post = get_object_or_404(Post.objects.all(), pk=pk)
        author = self.request.user
        data = request.data

        if self.request.method == 'POST':
            serializer = CreateCommentSerializer(data=data)

            if serializer.is_valid():
                serializer.save(author=author, post=post)
                return Response(serializer.data)

            else:
                return Response(status=400)

        if self.request.method == 'DELETE':
            comment_pk = data['pk']
            comment_object = get_object_or_404(EventComment.objects.all(), pk=comment_pk)
            comment_object.delete()
            return Response(status=200)





    #saves an event to a users account
    @detail_route(methods=['get', 'post', 'delete'])
    def save(self, request, pk=None):
        event = get_object_or_404(Post.objects.all(), pk=pk)
        requesting_user = get_object_or_404(Account.objects.all(), user=request.user)

        if request.method == 'POST':
            if requesting_user in event.attending.all():
                    return Response({'detail': 'You are already attending this event'}, status=status.HTTP_403_FORBIDDEN)

            event.attending.add(requesting_user)

            #signal to add notification to the notification feed
            notify.send(request.user, recipient=event.author, verb='saved', action_object=event)

            #send the user that was sent a follow request a notification
            if get_object_or_404(FCMDevice.objects.all(), user=event.author):
                device = get_object_or_404(FCMDevice.objects.all(), user=event.author)
                message = request.user.username + " saved your event"
                device.send_message(title="One more person saved your event", body=message)

            return Response(status=200)


        if request.method == 'DELETE':

            # remove from attending list
            event.attending.remove(requesting_user)
            event.save()
            return Response(status=200)

    #returns the accounts that saved an event
    @detail_route(methods=['get'])
    def people_saving(self, request, pk=None):
        event = get_object_or_404(Post.objects.all(), pk=pk)
        #requesting_user = get_object_or_404(Account.objects.all(), user=request.user)

        if request.method == 'GET':
            serializer = AccountSerializer(event.attending, context={'request': request}, many=True)
            return Response(serializer.data)



class PostTodayViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.filter(date=date.today()).order_by('time')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)



#includes a nested user model instead of just the username like the
class FilteredEventViewSet(viewsets.ModelViewSet):

    startdate = date.today()
    enddate = startdate + timedelta(days=365)

    queryset = Post.objects.filter(date__range=[startdate, enddate]).order_by('-posted_date')
    now = timezone.localtime(timezone.now())
    #queryset = Post.objects.filter(posted_date__lte=timezone.now()).filter(Q(date__gte=now.date())).order_by('-posted_date')
    serializer_class = EventSerializer
    parser_classes = (MultiPartParser, JSONParser)

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    model = Post



#returns the requesting users feed based on the people they are following
class FeedViewSet(viewsets.ModelViewSet):

    query = Account.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        account = get_object_or_404(self.query, user=self.request.user)
        following = account.following.values_list('user', flat=True)
        date_joined = self.request.user.date_joined

        return Post.objects.filter(author__in=following, author=self.request.user, date__gt=date_joined).order_by('-posted_date')


#returns the requesting users account instance
class MyAccountViewSet(viewsets.ModelViewSet):

    queryset = Account.objects.all()
    serializer_class =  AccountSerializer
    parser_classes = (MultiPartParser, JSONParser)
    permission_classes = (IsOwnerOrReadOnlyAccount,)
    model = Account

    def get_queryset(self):
        user = self.request.user
        return Account.objects.filter(user=user)


    '''
    def myposted(self):
        user = self.request.user
        return Post.objects.filter(author=user)

    def mysaved(self):
        user=self.request.user
        account = get_object_or_404(Account.objects.all(), user=user)
        return account.attending.all()
    '''

class MyRecommendedViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class =  AccountSerializer
    parser_classes = (MultiPartParser, JSONParser)
    permission_classes = (IsOwnerOrReadOnlyAccount,)
    model = Account

    def get_queryset(self):
        user = self.request.user
        account = get_object_or_404(self.queryset, user=user)
        mycollege = account.college
        following = account.following.all()
        following_user =[]
        requested_user = []
        for i in following:
            following_user.append(i.user)

        requested = account.requested.all()
        for i in requested:
            requested_user.append(i.user)


        #num_posted = Post.objects.filter(author=user).count()
        #annotate(followers_count=Count('followers')).
        recommended = Account.objects.filter(college=mycollege).exclude(user__in=requested_user).exclude(user__in=following_user).exclude(user=self.request.user).select_related('user').prefetch_related('following').prefetch_related('requesting')
        return sorted(recommended, key= lambda t: t.num_posted, reverse=True)[:20]



class OrganizationsViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.filter(organization=True)
    serializer_class = AccountSerializer
    parser_classes = (MultiPartParser, JSONParser)
    permission_classes = (IsOwnerOrReadOnlyAccount,)
    model = Account



class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all().select_related('user').prefetch_related('following').prefetch_related('requesting')
    serializer_class =  AccountSerializer
    parser_classes = (MultiPartParser, JSONParser)
    permission_classes = (IsOwnerOrReadOnlyAccount,)
    model = Account
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username', 'user__first_name', 'user__last_name',)


    @detail_route(methods=['get'])
    def saved(self, request, pk=None):
        account = get_object_or_404(self.queryset, pk=pk)
        if request.method == 'GET':
            serializer = EventSerializer(account.attending, context={'request': request}, many=True)
            return Response(serializer.data)

    @detail_route(methods=['get'])
    def posted(self, request, pk=None):
        account = get_object_or_404(self.queryset, pk=pk)
        user = account.user
        query = Post.objects.filter(author=user)

        if request.method == 'GET':
            serializer = EventSerializer(query, context={'request': request}, many=True)
            return Response(serializer.data)



    @detail_route(methods=['post'])
    def update_profile(self, request, *args, **kwargs):
        data = request.data
        user = get_object_or_404(self.queryset, user=request.user)
        serializer = AccountSerializer(user, data=data, context={'request': request}, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)


    #get the account's followers
    @detail_route(methods=['get'])
    def followers(self, request, pk=None):

        account = get_object_or_404(self.queryset, pk=pk)
        if request.method == 'GET':
            serializer = AccountSerializer(account.followers, context={'request': request}, many=True)
            return Response(serializer.data)

    #get the people the account is following
    @detail_route(methods=['get'])
    def following(self, request, pk=None):

        account = get_object_or_404(self.queryset, pk=pk)
        if request.method == 'GET':
            serializer = AccountSerializer(account.following, context={'request': request}, many=True)
            return Response(serializer.data)

    #get the people requesting to follow the account
    @detail_route(methods=['get'])
    def requesting(self, request, pk=None):

        account = get_object_or_404(self.queryset, pk=pk)
        if request.method == 'GET':
            serializer = AccountSerializer(account.requesting, context={'request': request}, many=True)
            return Response(serializer.data)

    #get the people the account has requested to folloq
    @detail_route(methods=['get'])
    def requested(self, request, pk=None):

        account = get_object_or_404(self.queryset, pk=pk)
        if request.method == 'GET':
            serializer = AccountSerializer(account.requested, context={'request': request}, many=True)
            return Response(serializer.data)


    #function that handles the following/unfollowing
    @detail_route(methods=['post', 'put', 'get', 'delete'])
    def follow(self, request, pk=None):

        url_user = get_object_or_404(self.queryset, pk=pk) #user from url
        requesting_user = get_object_or_404(self.queryset, user=request.user)  #requesting user

        if request.method == 'GET':
            serializer = AccountSerializer(url_user.requested, context={'request': request}, many=True)
            return Response(serializer.data)

        # send follow request
        if request.method == 'POST':
            if request.user.pk is int(pk):  # cant add yourself as your friend
                return Response({'detail': 'cant follow yourself'}, status=status.HTTP_403_FORBIDDEN)
            else:
                if requesting_user in url_user.followers.all():
                    return Response({'detail': 'Already following'}, status=status.HTTP_403_FORBIDDEN)

                if url_user in requesting_user.requested.all():
                    return Response({'detail': 'Already sent the request'}, status=status.HTTP_403_FORBIDDEN)

                requesting_user.requested.add(url_user)

                #signal to add notification to the notification feed

                notify.send(request.user, recipient=url_user, verb='has requested to follow you')

                #send the user that was sent a follow request a notification
                if get_object_or_404(FCMDevice.objects.all(), user=url_user):
                    device = get_object_or_404(FCMDevice.objects.all(), user=url_user)
                    #device.send_message("Title", "Message")
                    #device.send_message(data={"test": "test"})
                    message = request.user.username + " has requested to follow you"
                    #device.send_message(title="You have one new follow request", body=message, icon=..., data={"test": "test"})
                    device.send_message(title="You have one new follow request", body=message)


                return Response(status=200)


        if request.method == 'PUT':
            if request.user.pk is int(pk):  # cant add yourself as your friend
                return Response({'detail': 'cant follow yourself'}, status=status.HTTP_403_FORBIDDEN)
            else:
                if url_user not in requesting_user.requesting.all():
                    return Response({'detail': 'No follow request found'}, status=status.HTTP_403_FORBIDDEN)

                requesting_user.followers.add(url_user)
                requesting_user.requesting.remove(url_user)
                url_user.following.add(requesting_user)

                #signal to add notification to the notification feed
                notify.send(request.user, recipient=url_user, verb='has accepted your follow request')

                #send the user that sent a follow request a notification
                if get_object_or_404(FCMDevice.objects.all(), user=url_user):
                    device = get_object_or_404(FCMDevice.objects.all(), user=url_user)
                    message = request.user.username + " has accepted your follow request"
                    device.send_message(title=message)

                return Response(status=200)


        if request.method == 'DELETE':

            # remove from user follow list or waitlist if the user's request hadnt been accepted yet
            url_user.followers.remove(requesting_user)
            url_user.requesting.remove(requesting_user)

            requesting_user.following.remove(url_user)
            requesting_user.requested.remove(url_user)
            requesting_user.save()
            url_user.save()
            return Response(status=200)


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

    queryset = Post.objects.filter(Q(category = Post.DANCE) | Q(category=Post.PERFORMING_ARTS)  | Q(category=Post.ARTS) | Q(category = Post.THEATRE)).order_by('-posted_date')
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





