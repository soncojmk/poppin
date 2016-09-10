from rest_framework import serializers
from Post.models import Post
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'street_address', 'city', 'state', 'zip_code', 'date', 'time', 'description', 'price', 'image')


class UserSerializer(serializers.ModelSerializer):
    #posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'author')

author = serializers.ReadOnlyField(source='author.username')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ('url', 'pk', 'author',
                  'title', 'street_address', 'city', 'state', 'zip_code', 'date', 'time', 'description', 'price', 'image')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    #posts = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'pk', 'username')