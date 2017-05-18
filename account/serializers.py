from rest_framework import serializers
from account.models import Account
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from stdimage.models import StdImageField
from drf_extra_fields.fields import Base64ImageField


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class followingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('following',)

class requestingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('requesting',)


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    following = followingSerializer(read_only=True, many=True)
    requesting = requestingSerializer(read_only=True, many=True)
    user = UserSerializer()
    avatar = Base64ImageField(required=False)

    class Meta:
        model = Account
        fields = ('url', 'user', 'avatar', 'about', 'college', 'following', 'requesting', 'num_followers','num_following', 'num_requesting')


    #this only creates the user model not the account one. We however only need to use the other authentication model to create users
    #we use this serializer to create update a user's account
    def create(self, attrs):
        user = attrs.pop('user')
        user = User.objects.create(**user)
        about = attrs.get('about')
        college = attrs.get('college')
        account = Account(user=user, about=about, college=college)
        account.save()

        return account

    #this works

    def update(self, instance, attrs):

        #request = self.context['request']
        instance.about = attrs.get('about', instance.about)
        instance.avatar = attrs.get('avatar', instance.avatar)
        instance.college =attrs.get('college', instance.college)


        instance.save()
        return instance



