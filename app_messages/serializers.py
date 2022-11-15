from django.contrib.auth.models import User
from rest_framework import serializers
from .models import AppMessage


class AppMessageReciverPKField(serializers.PrimaryKeyRelatedField):
    """
    Class to order the reciver choise to
    show all users that the sender is following
    first
    """
    def get_queryset(self):
        user = self.context['request'].user
        queryset = User.objects.all().order_by('followed')
        return queryset


class AppMessageSerializer(serializers.ModelSerializer):
    """
    Serializer class for AppMessages
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    reciver = serializers.ReadOnlyField(source='reciver.username')
    is_reciver = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_is_reciver(self, obj):
        request = self.context['request']
        return request.user == obj.reciver

    class Meta:
        model = AppMessage
        fields = [
            'id', 'owner', 'reciver', 'is_owner',
            'is_reciver', 'subject', 'sent', 'content'
            'profile_id', 'profile_image']


class CreateAppMessageSerializer(serializers.ModelSerializer):
    """
    Serializer class for AppMessages
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    reciver = AppMessageReciverPKField()

    class Meta:
        model = AppMessage
        fields = '__all__'
