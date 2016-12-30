from django.contrib import admin
from .models import Post, EventComment, QuestionComment, Question, Concert, ConcertComment, Survey, Broadcast_Email

# Register your models here.


from django.utils.safestring import mark_safe
import threading
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import (send_mail, BadHeaderError, EmailMessage)
from django.contrib.auth.models import User

class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, settings.EMAIL_HOST_USER, self.recipient_list)
        msg.content_subtype = "html"
        try:
            msg.send()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

class BroadCast_Email_Admin(admin.ModelAdmin):
    model = Broadcast_Email

    def submit_email(self, request, obj): #`obj` is queryset, so there we only use first selection, exacly obj[0]
        list_email_user = [ p.email for p in User.objects.all() ] #: if p.email != settings.EMAIL_HOST_USER   #this for exception
        obj_selected = obj[0]
        EmailThread(obj_selected.subject, mark_safe(obj_selected.message), list_email_user).start()
    submit_email.short_description = 'Submit BroadCast (1 Select Only)'
    submit_email.allow_tags = True

    actions = [ 'submit_email' ]

    list_display = ("subject", "created")
    search_fields = ['subject',]

admin.site.register(Broadcast_Email, BroadCast_Email_Admin)

admin.site.register(Post)
admin.site.register(EventComment)
admin.site.register(QuestionComment)
admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Concert)
admin.site.register(ConcertComment)
#admin.site.register(Broadcast_Email)
