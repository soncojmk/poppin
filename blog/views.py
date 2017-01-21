from django.shortcuts import render

from django.shortcuts import render, redirect
from django.utils import timezone
from django.shortcuts import get_object_or_404, render_to_response
from .forms import PostForm
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

from .models import Blog

# Create your views here.

def blog_list(request):
    posts = Blog.objects.filter(posted_date__lte=timezone.now()).order_by('-posted_date')
    return render(request, 'post_list.html', {'posts':posts})

def blog_detail(request, pk):
    post = get_object_or_404(Blog, pk=pk)

    context = {
        'post':post,
    }
    return render(request, 'post_detail.html', context)

@login_required
def blog_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.posted_date = timezone.now()
            post.save()
            return redirect('blog_list')
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})

@login_required
def blog_edit(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.posted_date = timezone.now()
            post.save()
            return redirect('blog_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})


@login_required
def blog_remove(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    return redirect('blog.views.blog_list')

