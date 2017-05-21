from activity_stream import forms
#from activity_stream.models import Item
from activity_stream.models import Follow
from django.contrib.auth import authenticate, get_user_model, \
    login as auth_login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
#from stream_django.feed_manager import feed_manager
#from activity_stream.enrich import Enrich
#from activity_stream.enrich import do_i_follow_users
import json


def redirect_to_next(request):
    return HttpResponseRedirect(request.POST.get('next', '/'))


def render_output(output):
    ajax_response = HttpResponse(
        json.dumps(output), content_type='application/json')
    return ajax_response


def trending(request):
    '''
    The most popular items
    '''
    if not request.user.is_authenticated() and not settings.USE_AUTH:
        # hack to log you in automatically for the demo app
        admin_user = authenticate(username='admin', password='admin')
        auth_login(request, admin_user)

    # show a few items
    context = RequestContext(request)
    popular = Item.objects.all()[:50]
    if request.user.is_authenticated():
        did_i_pin_items(request.user, popular)
    context['popular'] = popular
    response = render_to_response('activity_stream/trending.html', context)
    return response

"""
@login_required
def feed(request):
    '''
    Items pinned by the people you follow
    '''
    enricher = Enrich(request.user)
    context = RequestContext(request)
    feed = feed_manager.get_news_feeds(request.user.id)['timeline']
    activities = feed.get(limit=25)['results']
    context['activities'] = enricher.enrich_activities(activities)
    response = render_to_response('activity_stream/feed.html', context)
    return response


@login_required
def aggregated_feed(request):
    '''
    Items pinned by the people you follow
    '''
    enricher = Enrich(request.user)
    context = RequestContext(request)
    feed = feed_manager.get_news_feeds(request.user.id)['aggregated']
    activities = feed.get(limit=25)['results']
    context['activities'] = enricher.enrich_aggregated_activities(activities)
    response = render_to_response('activity_stream/aggregated_feed.html', context)
    return response


@login_required
def notification_feed(request):
    enricher = Enrich(request.user)
    context = RequestContext(request)
    feed = feed_manager.get_notification_feed(request.user.id)
    activities = feed.get(limit=25, mark_seen='all')['results']
    context['activities'] = enricher.enrich_aggregated_activities(activities)
    response = render_to_response('activity_stream/notification_feed.html', context)
    return response


def profile(request, username):
    '''
    Shows the users profile
    '''
    enricher = Enrich(request.user)
    profile_user = get_user_model().objects.get(username=username)
    feed = feed_manager.get_user_feed(profile_user.id)
    activities = feed.get(limit=25)['results']
    context = RequestContext(request)
    do_i_follow_users(request.user, [profile_user])
    context['profile_user'] = profile_user
    context['activities'] = enricher.enrich_activities(activities)
    response = render_to_response('activity_stream/profile.html', context)
    return response


@login_required
def people(request):
    context = RequestContext(request)
    people = get_user_model().objects.all()
    people = people.exclude(username__in=['admin', 'bogus'])
    people = people[:]
    do_i_follow_users(request.user, people)
    context['people'] = people
    response = render_to_response('activity_stream/people.html', context)
    return response



@login_required
def follow(request):
    '''
    A view to follow other users
    '''
    output = {}
    if request.method == "POST":
        form = forms.FollowForm(user=request.user, data=request.POST)

        if form.is_valid():
            follow = form.save()
            if follow:
                output['follow'] = dict(id=follow.id)
            if not request.is_ajax():
                return redirect_to_next(request)
        else:
            output['errors'] = dict(form.errors.items())
    return HttpResponse(json.dumps(output), content_type='application/json')

"""
