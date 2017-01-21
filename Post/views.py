# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post, EventComment, QuestionComment, Question, Concert, ConcertComment, Survey
from django.shortcuts import get_object_or_404, render_to_response
from .forms import PostForm, EventCommentForm, QuestionCommentForm, QuestionForm, ConcertForm, ConcertCommentForm, SurveyForm, BroadCastForm
#from allauth.account.decorators import verified_email_required
from haystack.generic_views import SearchView
from toggles.views import ToggleView
from datetime import date
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from django.db.models import CharField
from django.db.models import Value
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
import account.forms
import account.views

from el_pagination.decorators import page_template

from datetime import date, timedelta

from django.views.generic.dates import TodayArchiveView, WeekArchiveView
#from django.views.generic.list_detail import object_list

from urllib2 import URLError

from django.contrib.gis import geos
from django.contrib.gis import measure
from django.shortcuts import render_to_response
from django.template import RequestContext
from geopy.geocoders import GoogleV3

from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.gis.geos import Point
from djgeojson.serializers import Serializer as GeoJSONSerializer

from django.db.models import Q

from django.http import HttpResponse
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
#from geopy.geocoders import GQueryError

# Create your views here.

'''mass email'''
def send_email(request):

    from_email = "What'sPoppin@wpoppin.com"
    to = []

    for user in User.objects.all():
        email = str.strip(str(user.email))
        to.append(email)



    email = BroadCastForm(request.POST)

    email.created = timezone.now()
    subject = "Events This Week"

    text_content = 'This is an important message.'
    html_content = '<div style="width: 660px; margin: auto; text-align: left; font-size: 15px; color: #504849; padding: 20px 20px 5px 20px;"><h1>What&#39;sPoppin Penn State! </h1><h4 style="color:grey;">Be on the look out for What&#39;sPoppin App Launch in two weeks. Check out some of this week&#39;s events below. More on wpoppin.com</h4><div class="well" style="background-color: white; border-top: .5px; border-left: 0px; border-right: 0px; border-bottom: solid lightgrey .5px; border-radius: 0px; margin-bottom: 15px; padding-bottom: 5px; width: 100%;"><p style="color: light-grey; text-align: left; font-size: 12px;">&nbsp;</p><p style="font-size: 15px; text-align: left;"><a style="font-size: 20px;" href="http://wpoppin.com/account/login"> <span style="font-size: 20px; color: #236b8e;">Involvement Fair</span></a><span style="float: right; color: grey;"> Free </span></p><p style="color: grey;"><p style="color: grey;">Get involved at Penn State! Find clubs and organizations you&#39;re interested in.</p><div class="image"><a href="http://wpoppin.com/account/login"><img class="img-responsive img-center" src="http://wpoppin.com/site_media/media/Post/images/involvement.large.JPG" alt="" /></a></div><p id="right" class="date"><a href="http://wpoppin.com/account/login">More information... </a></p></div><h4>&nbsp;</h4><div class="well" style="background-color: white; border-top: .5px; border-left: 0px; border-right: 0px; border-bottom: solid lightgrey .5px; border-radius: 0px; margin-bottom: 15px; padding-bottom: 5px; width: 100%;"><p style="color: light-grey; text-align: left; font-size: 12px;">&nbsp;</p><p style="font-size: 15px; text-align: left;"><a style="font-size: 20px;" href="http://wpoppin.com/account/login"> <span style="font-size: 20px; color: #236b8e;">Ballroom Dance Lessons</span></a><span style="float: right; color: grey;"> Free </span></p><p style="color: grey;">Dances Covered: Two Step, Waltz, Tango, Quickstep, Rumba, Cha Cha, Jive. All experience levels welcome. The beginner lesson provides an introduction to ballroom dancing. Lessons are based around giving dancers a basic knowledge of all dances with the goal of feeling comfortable dancing in social settings.</p><div class="image"><a href="http://wpoppin.com/account/login"><img class="img-responsive img-center" src="http://www.wpoppin.com/site_media/media/Post/images/ballroom-dance-feet2.large.jpg" alt="" /></a></div><p id="right" class="date"><a href="http://wpoppin.com/account/login">More information... </a></p></div><div class="well" style="background-color: white; border-top: .5px; border-left: 0px; border-right: 0px; border-bottom: solid lightgrey .5px; border-radius: 0px; margin-bottom: 15px; padding-bottom: 5px; width: 100%;"><p style="color: light-grey; text-align: left; font-size: 12px;">&nbsp;</p><p style="font-size: 15px; text-align: left;"><a style="font-size: 20px;" href="http://wpoppin.com/account/login"> <span style="font-size: 20px; color: #236b8e;">RAM Squad Dance Practice</span></a><span style="float: right; color: grey;"> Free </span></p><p style="color: grey;">It&#39;s never too late to join RAM - all you have to do is come to one of our practices. See you there 😄</p><div class="image"><a href="http://wpoppin.com/account/login"><img class="img-responsive img-center" src="http://www.wpoppin.com/site_media/media/Post/images/ramSquad.large.jpg" alt="" /></a></div><p id="right" class="date"><a href="http://wpoppin.com/account/login">More information... </a></p></div><div><p><a href="http://wpoppin.com/account/login">More Events...</a></p></div></div>'
    #'<div style="width:660px;margin:auto;text-align:left; font-size: 15px; color: #504849; padding-left:20px; padding-right:20px; padding-bottom:5px; padding-top: 20px;"> <h1>What&#39;sPoppin Penn State, </h1><h4>Check out these events poppin this week around campus:<h4> <div class="well"  style="background-color: white; border-top: .5px; border-left: 0px; border-right: 0px; border-bottom: solid lightgrey .5px; border-radius: 0px; margin-bottom:15px; padding-bottom: 5px; width:100%;"><p style="color:light-grey; text-align:left; font-size: 12px; "></p><p style = "font-size:15px; text-align:left;"><a style = "font-size:20px; " href="http://wpoppin.com"> <span style = "font-size:20px; color:#236B8E;">What&#39;sPoppin: Debate Night</span></a><span style="float:right;  color:grey;"> Free </span></p><p class="text" style=" text-align:left;  font-size:15px; color: #504849;  padding-bottom:5px;"><p style="color:grey;">Willard Preacher vs Sam Richards Debate! </p><p style="color:grey;">You do not want to miss the event of the semester. Come out and watch the Willard Preacher take on Sam Richards as they debate various topics, which if you&#39;ve passed by the Willard building, you already know what they are.</p></p><div class= "image"><a   href="http://wpoppin.com"><img style= "   "class="img-responsive img-center" alt=""  src="http://wpoppin.com/site_media/media/Post/images/willardPreacher.large.jpg"/></a></div><p class="date" id="right"> Mon 28 Nov 2016 7 p.m. </p></div> <br> <div class="well"  style="background-color: white; border-top: .5px; border-left: 0px; border-right: 0px; border-bottom: solid lightgrey .5px; border-radius: 0px; margin-bottom:15px; padding-bottom: 5px; width:100%;"><p style="color:light-grey; text-align:left; font-size: 12px; "></p><p style = "font-size:15px; text-align:left;"><a style = "font-size:20px; " href="http://wpoppin.com"> <span style = "font-size:20px; color:#236B8E;">Saturday School Exhibition</span></a><span style="float:right;  color:grey;"> Free </span></p><p class="text" style=" text-align:left;  font-size:15px; color: #504849;  padding-bottom:5px;"><p style="color:grey;">Artworks created by students in SoVA&#39;s FA16 Saturday School Program</p><p style="color:grey;">10:00 am - 4:00 pm</p> </p></p><div class= "image"><a   href="http://wpoppin.com"><img style= "   "class="img-responsive img-center" alt=""  src="http://www.wpoppin.com/site_media/media/Post/images/date_night_sRu9dkw.large.jpg"/></a></div><p class="date" id="right"> Mon 28 Nov 2016 10 a.m - 4:00 pm. </p></div></div>'

    msg = EmailMultiAlternatives(subject, text_content, from_email, [], to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


    return render(request, 'Post/email_edit.html', {'email': email})




''' categories '''
def music(request):
    posts = Post.objects.filter(category = Post.MUSIC).order_by('-posted_date')
    return render(request, 'Post/music.html', {'posts':posts})

def sports(request):
    posts = Post.objects.filter(category = Post.SPORTS).order_by('-posted_date')
    return render(request, 'Post/sports.html', {'posts':posts})

def charity(request):
    posts = Post.objects.filter(category = Post.FUNDRAISERS).order_by('-posted_date')
    return render(request, 'Post/charity.html', {'posts':posts})

def art(request):
    posts = Post.objects.filter(category = Post.ART).order_by('-posted_date')
    return render(request, 'Post/Art.html', {'posts':posts})

def comedy(request):
    posts = Post.objects.filter(category = Post.COMEDY).order_by('-posted_date')
    return render(request, 'Post/comedy.html', {'posts':posts})

def poetry(request):
    posts = Post.objects.filter(category = Post.POETRY).order_by('-posted_date')
    return render(request, 'Post/poetry.html', {'posts':posts})


def performing_arts(request):
    posts = Post.objects.filter(Q(category = Post.DANCE) | Q(category=Post.ARTS) | Q(category = Post.THEATRE)).order_by('-posted_date')
    return render(request, 'Post/arts.html', {'posts':posts})

def academic(request):
    posts = Post.objects.filter(Q(category = Post.ACADEMIC) | Q(category=Post.PROFESSIONAL) | Q(category = Post.CLUB_EVENT) | Q(category = Post.LECTURE) | Q(category = Post.DEBATE)).order_by('-posted_date')
    return render(request, 'Post/academic.html', {'posts':posts})

def wpoppin(request):
    posts = Post.objects.filter(category = Post.WP).order_by('-posted_date')
    return render(request, 'Post/wp.html', {'posts': posts})


'''end categories'''


def survey(request):
    if request.method == "POST":
        form = SurveyForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.date = timezone.now()
            post.save()
            return redirect('home')
    else:
        form = SurveyForm()
    return render(request, 'homepage.html', {'form': form})



def EventsToday(request):
    posts = Post.objects.filter(date=date.today()).order_by('time')
    return render(request, 'Post/post_archive_day.html', {'posts':posts})


def EventsTomorrow(request):
    today = date.today()
    startdate = today + timedelta(days=1)
    enddate = startdate + timedelta(days=2)

    posts = Post.objects.filter(date__range=[startdate, enddate]).order_by('date')
    return render(request, 'Post/post_tomorrow.html', {'posts':posts})


def EventsWeek(request):
    startdate = date.today()
    enddate = startdate + timedelta(days=6)

    posts = Post.objects.filter(date__range=[startdate, enddate]).order_by('date')
    return render(request, 'Post/post_this_week.html', {'posts':posts})


def EventsMonth(request):
    startdate = date.today()
    enddate = startdate + timedelta(days=30)

    posts = Post.objects.filter(date__range=[startdate, enddate]).order_by('date')
    return render(request, 'Post/post_this_month.html', {'posts':posts})


class ConcertsToday(TodayArchiveView):
    queryset = Concert.objects.all()
    date_field = "date"
    allow_future = True

def FeedToday(request):
    # annotate a type for each model to be used in the template
    events = Post.objects.filter(date=date.today()).annotate(type=Value('events', CharField())).order_by('time')
    #questions = Question.objects.filter(posted_date__lte == datetime.now().date).annotate(type=Value('questions', CharField()))
    concerts = Concert.objects.filter(date=date.today()).annotate(type=Value('concerts', CharField())).order_by('time')


    all_items = list(events) + list(concerts)

    # all items sorted by publication date. Most recent first
    all_items_feed = sorted(all_items, key=lambda obj: obj.time)
    #all_items_feed.reverse()

    return render(request, 'Post/feed_today.html', {'all_items_feed': all_items_feed})


def FeedTomorrow(request):
    # annotate a type for each model to be used in the template
    today = date.today()
    startdate = today + timedelta(days=1)
    enddate = startdate + timedelta(days=2)

    events = Post.objects.filter(date__range=[startdate, enddate]).annotate(type=Value('events', CharField())).order_by('-date')
    #questions = Question.objects.filter(posted_date__lte == datetime.now().date).annotate(type=Value('questions', CharField()))
    concerts = Concert.objects.filter(date__range=[startdate, enddate]).annotate(type=Value('concerts', CharField())).order_by('-date')


    all_items = list(events) + list(concerts)

    # all items sorted by publication date. Most recent first
    all_items_feed = sorted(all_items, key=lambda obj: obj.posted_date)
    all_items_feed.reverse()

    return render(request, 'Post/feed_tomorrow.html', {'all_items_feed': all_items_feed})


def FeedWeek(request):
    # annotate a type for each model to be used in the template
    startdate = date.today()
    enddate = startdate + timedelta(days=6)

    events = Post.objects.filter(date__range=[startdate, enddate]).annotate(type=Value('events', CharField())).order_by('-date')
    #questions = Question.objects.filter(posted_date__lte == datetime.now().date).annotate(type=Value('questions', CharField()))
    concerts = Concert.objects.filter(date__range=[startdate, enddate]).annotate(type=Value('concerts', CharField())).order_by('-date')


    all_items = list(events) + list(concerts)

    # all items sorted by publication date. Most recent first
    all_items_feed = sorted(all_items, key=lambda obj: obj.posted_date)
    all_items_feed.reverse()

    return render(request, 'Post/feed_this_week.html', {'all_items_feed': all_items_feed})





def FeedMonth(request):
    # annotate a type for each model to be used in the template
    startdate = date.today()
    enddate = startdate + timedelta(days=30)

    events = Post.objects.filter(date__range=[startdate, enddate]).annotate(type=Value('events', CharField())).order_by('-date')
    #questions = Question.objects.filter(posted_date__lte == datetime.now().date).annotate(type=Value('questions', CharField()))
    concerts = Concert.objects.filter(date__range=[startdate, enddate]).annotate(type=Value('concerts', CharField())).order_by('-date')


    all_items = list(events) + list(concerts)

    # all items sorted by publication date. Most recent first
    all_items_feed = sorted(all_items, key=lambda obj: obj.posted_date)
    all_items_feed.reverse()

    return render(request, 'Post/feed_this_month.html', {'all_items_feed': all_items_feed})






def geocode_address(address):
    address = address.encode('utf-8')
    geocoder = GoogleV3()
    try:
        _, latlon = geocoder.geocode(address)
    except (URLError, ValueError):
        return None
    else:
        return latlon

def get_posts(lon, lat):
    current_point = geos.fromstr("POINT(%s %s)" % (lon, lat))
    distance_from_point = {'km': 10}
    posts = Post.gis.filter(location__distance_lte=(current_point, measure.D(**distance_from_point)))
    posts = posts.distance(current_point).order_by('distance')
    return posts.distance(current_point)

def location(request):

    if request.is_ajax():
        lat = request.GET.get('lat', None)
        lon = request.GET.get('lon', None)

        if lat and lon:
            posts = get_posts(lon, lat)
            geojson_data = GeoJSONSerializer().serialize(
                posts, use_natural_keys=True)


            return HttpResponse(geojson_data,
                mimetype='application/json')
    msg = "Bad request: not AJAX or no latlong pair present"
    return HttpResponseBadRequest(msg)


'''
@login_required
def post_list(request):
    posts = Post.objects.filter(posted_date__lte=timezone.now()).order_by('-posted_date')
    return render(request, 'Post/post_list.html', {'posts':posts})
'''

@login_required
@page_template('Post/post_list.html')  # just add this decorator
def post_list(
        request, template='Post/post_list_scroll.html', extra_context=None):
    context = {
        'posts': Post.objects.filter(posted_date__lte=timezone.now()).order_by('-posted_date'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))




def post_detail(request, pk):
    form = EventCommentForm()
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = EventCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = EventCommentForm()

    context = {
        'form':form,
        'post':post,
    }

    return render(request, 'Post/post_detail.html', context)

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.posted_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'Post/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.posted_date = timezone.now()
            post.created_at = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'Post/post_edit.html', {'form': form})


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('Post.views.post_list')



class MySearchView(SearchView):
    """My custom search view."""

    def get_queryset(self):
        queryset = super(MySearchView, self).get_queryset()
        # further filter queryset based on some set of criteria
        return queryset.filter(pub_date__gte=date(2015, 1, 1))

    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        # do something
        return context

def categories(request):
    tags = get_object_or_404(Tag.name)
    posts = Post.objects.filter(tags__name__in=[tags])
    return render(request, 'Post/tagpage.html', {'posts':posts})

'''
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)
'''

@login_required
def event_comment_remove(request, pk):
    comment = get_object_or_404(EventComment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)



'''
def category_list(request):
    categories = Category.objects.all() # this will get all categories, you can do some filtering if you need (e.g. excluding categories without posts in it)

    return render (request, 'post/post_list.html', {'categories': categories}) # blog/category_list.html should be the template that categories are listed.

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)

    return render(request, 'post/post_list.html', {'category': category}) # in this template, you will have access to category and posts under that category by (category.post_set).
'''
@login_required
def question_list(request):
    questions = Question.objects.filter(posted_date__lte=timezone.now()).order_by('-posted_date')
    form = QuestionForm()

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.posted_date = timezone.now()
            question.save()
            return redirect('question_list')
    else:
        form = QuestionForm()

    context = {
        'form':form,
        'questions':questions,
    }

    return render(request, 'Post/question_list.html', context)


def question_detail(request, pk):
    form = QuestionCommentForm()
    question = get_object_or_404(Question, pk=pk)


    if request.method == "POST":
        form = QuestionCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.question = question
            comment.save()
            return redirect('question_detail', pk=question.pk)
    else:
        form = QuestionCommentForm()


    context = {
        'form':form,
        'question':question,

    }

    return render(request, 'Post/question_detail.html', context)

@login_required
def question_new(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.posted_date = timezone.now()
            question.save()
            return redirect('question_list')
    else:
        form = QuestionForm()
    return render(request, 'Post/question_edit.html', {'form': form})

@login_required
def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            #question.photo = request.FILES['photo']
            question.posted_date = timezone.now()
            question.created_at = timezone.now()
            question.save()
            return redirect('question_list')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'Post/question_edit.html', {'form': form})


@login_required
def question_remove(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.delete()
    return redirect('question_list')

@login_required
def question_comment_remove(request, pk):
    comment = get_object_or_404(QuestionComment, pk=pk)
    question_pk = comment.question.pk
    comment.delete()
    return redirect('question_detail', pk=question_pk)

@login_required
def feed(request):
    # annotate a type for each model to be used in the template
    events = Post.objects.all().annotate(type=Value('events', CharField()))
    questions = Question.objects.all().annotate(type=Value('questions', CharField()))
    concerts = Concert.objects.all().annotate(type=Value('concerts', CharField()))


    all_items = list(events) + list(questions) + list(concerts)

    # all items sorted by publication date. Most recent first
    all_items_feed = sorted(all_items, key=lambda obj: obj.posted_date)
    all_items_feed.reverse()

    return render(request, 'Post/feed.html', {'all_items_feed': all_items_feed})




@login_required
def my_events(request):
    posts = Post.objects.filter(posted_date__lte=timezone.now()).order_by('-posted_date')
    return render(request, 'Post/my_events.html', {'posts':posts})

@login_required
def my_questions(request):
    questions = Question.objects.filter(posted_date__lte=timezone.now()).order_by('-posted_date')
    return render(request, 'Post/my_questions.html', {'questions':questions})



@login_required
def concert_list(request):
    concerts = Concert.objects.order_by('-date')
    return render(request, 'Post/concert_list.html', {'concerts':concerts})

def concert_detail(request, pk):
    form = ConcertCommentForm()
    concert = get_object_or_404(Concert, pk=pk)

    if request.method == "POST":
        form = ConcertCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.concert = concert
            comment.save()
            return redirect('concert_detail', pk=concert.pk)
    else:
        form = ConcertCommentForm()

    context = {
        'form':form,
        'concert':concert,
    }

    return render(request, 'Post/concert_detail.html', context)
@login_required
def concert_new(request):
    if request.method == "POST":
        form = ConcertForm(request.POST, request.FILES)
        if form.is_valid():
            concert = form.save(commit=False)
            concert.author = request.user
            concert.posted_date = timezone.now()
            concert.save()
            return redirect('concert_list')
    else:
        form = ConcertForm()
    return render(request, 'Post/concert_edit.html', {'form': form})

@login_required
def concert_edit(request, pk):
    concert = get_object_or_404(Concert, pk=pk)
    if request.method == "POST":
        form = ConcertForm(request.POST, request.FILES, instance=concert)
        if form.is_valid():
            concert = form.save(commit=False)
            concert.author = request.user
            concert.posted_date = timezone.now()
            concert.created_at = timezone.now()
            concert.save()
            return redirect('concert_list')
    else:
        form = ConcertForm(instance=concert)
    return render(request, 'Post/concert_edit.html', {'form': form})


@login_required
def concert_remove(request, pk):
    concert = get_object_or_404(Concert, pk=pk)
    concert.delete()
    return redirect('Post.views.concert_list')

@login_required
def concert_comment_remove(request, pk):
    comment = get_object_or_404(ConcertComment, pk=pk)
    concert_pk = comment.concert.pk
    comment.delete()
    return redirect('concert_detail', pk=concert_pk)

