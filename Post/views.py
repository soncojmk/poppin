from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post, EventComment, QuestionComment, Question
from django.shortcuts import get_object_or_404, render_to_response
from .forms import PostForm, EventCommentForm, QuestionCommentForm, QuestionForm
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
#from django.views.generic.list_detail import object_list
# Create your views here.


class LoginView(account.views.LoginView):

    form_class = account.forms.LoginEmailForm


def post_list(request):
    posts = Post.objects.filter(posted_date__lte=timezone.now()).order_by('-posted_date')
    return render(request, 'Post/post_list.html', {'posts':posts})

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


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'Post/post_edit.html', {'form': form})



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


def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            #question.photo = request.FILES['photo']
            question.published_date = timezone.now()
            question.save()
            return redirect('question_list')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'Post/question_edit.html', {'form': form})



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


def feed(request):
    # annotate a type for each model to be used in the template
    events = Post.objects.all().annotate(type=Value('events', CharField()))
    questions = Question.objects.all().annotate(type=Value('questions', CharField()))


    all_items = list(events) + list(questions)

    # all items sorted by publication date. Most recent first
    all_items_feed = sorted(all_items, key=lambda obj: obj.posted_date)
    all_items_feed.reverse()

    return render(request, 'Post/feed.html', {'all_items_feed': all_items_feed})

'''
def my_profile(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)

    return render(request, 'Post/my_profile.html', {'profile':profile})

def profile_new(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('my_profile', pk=profile.pk)
    else:
        form = UserProfileForm()
    return render(request, 'Post/profile_edit.html', {'form': form})


def profile_edit(request, pk):
    profile = get_object_or_404(UserProfile pk=pk)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('my_profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'Post/profile_edit.html', {'form': form})
'''




@login_required
def my_events(request):
    posts = Post.objects.filter(posted_date__lte=timezone.now()).order_by('-posted_date')
    return render(request, 'Post/my_events.html', {'posts':posts})

@login_required
def my_questions(request):
    questions = Question.objects.filter(posted_date__lte=timezone.now()).order_by('-posted_date')
    return render(request, 'Post/my_questions.html', {'questions':questions})




'''

class ProfileObjectMixin(SingleObjectMixin):
    """
    Provides views with the current user's profile.
    """
    model = Profile

    def get_object(self):
        """Return's the current users profile."""
        try:
            return self.request.user.get_profile()
        except Profile.DoesNotExist:
            raise NotImplemented(
                "What if the user doesn't have an associated profile?")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """Ensures that only authenticated users can access the view."""
        klass = ProfileObjectMixin
        return super(klass, self).dispatch(request, *args, **kwargs)


class ProfileUpdateView(ProfileObjectMixin, UpdateView):
    """
    A view that displays a form for editing a user's profile.

    Uses a form dynamically created for the `Profile` model and
    the default model's update template.
    """
    pass  # That's All Folks!

'''

