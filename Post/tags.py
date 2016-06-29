import datetime
from django.shortcuts import render, redirect
from django import template


from django.utils import timezone
from .models import Post, Comment
from django.shortcuts import get_object_or_404, render_to_response
from .forms import PostForm, CommentForm
#from allauth.account.decorators import verified_email_required
from haystack.generic_views import SearchView
from toggles.views import ToggleView
from datetime import date
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
# Create your views here.

register = template.Library()


@register.inclusion_tag('add_comment_to_post.html')
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        return commentForm()
