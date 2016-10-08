from django.contrib import admin
from .models import Post, EventComment, QuestionComment, Question, Concert, ConcertComment, Survey

# Register your models here.

admin.site.register(Post)
admin.site.register(EventComment)
admin.site.register(QuestionComment)
admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Concert)
admin.site.register(ConcertComment)
