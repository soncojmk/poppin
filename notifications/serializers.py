from rest_framework import serializers
from Post.models import Post
from account.models import Account
from Post.serializers import PostSerializer, UserSerializer
from account.serializers import AccountSerializer
from django.contrib.auth.models import User
from .models import Notification

class GenericNotificationRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        if isinstance(value, User):
            serializer = UserSerializer(value)
        if isinstance(value, Post):
            serializer = PostSerializer(value)

        return serializer.data


class NotificationSerializer(serializers.Serializer):
    actor = serializers.ReadOnlyField(source='actor.username')
    actor_account = AccountSerializer()
    recipient = serializers.ReadOnlyField(source='recipient.username')
    recipient_account = AccountSerializer()
    action_object_event = PostSerializer()
    unread = serializers.BooleanField(read_only=True)
    target = GenericNotificationRelatedField(read_only=True)
    verb = serializers.ReadOnlyField()

    class Meta:
        model = Notification
        fields = ('actor_account', 'verb', 'recipient_account', 'unread', 'target', 'action_object_event')

    def create(self, validated_data):
        return Notification.objects.create(**validated_data)