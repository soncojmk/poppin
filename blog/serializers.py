from rest_framework import serializers
from blog.models import Blog
from django.contrib.auth.models import User

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'price', 'image')


class BlogSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Blog
        fields = ('url', 'pk', 'author',
                  'title', 'description', 'image')

