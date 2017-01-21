from rest_framework import serializers
from Post.models import Post
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','category', 'title', 'street_address', 'city', 'state', 'zip_code', 'date', 'time', 'description', 'price', 'image', 'ticket_link')


class UserSerializer(serializers.ModelSerializer):
    #posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'author')

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST'
                else IsStaffOrTargetUser()),

author = serializers.ReadOnlyField(source='author.username')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ('url', 'pk', 'author', 'category',
                  'title', 'street_address', 'city', 'state', 'zip_code', 'date', 'time', 'description', 'price', 'image', 'ticket_link')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    #posts = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'pk', 'username')