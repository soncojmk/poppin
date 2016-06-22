from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post
from django.shortcuts import get_object_or_404, render_to_response
from .forms import PostForm
#from allauth.account.decorators import verified_email_required
from haystack.generic_views import SearchView
from toggles.views import ToggleView
from datetime import date
from django.core.urlresolvers import reverse
from taggit.models import Tag
# Create your views here.

def post_list(request):
    posts = Post.objects.filter(posted_date__lte=timezone.now()).order_by('posted_date')
    return render(request, 'Post/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'Post/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.posted_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'Post/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.photo = request.FILES['photo']
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
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
    #tag = get_object_or_404(Tag)
    posts = Post.objects.filter(tags__name__in=["soccer"])
    return render(request, 'Post/tagpage.html', {'posts':posts})

