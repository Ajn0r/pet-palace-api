from rest_framework import serializers
from .models import AppMessage


class AppMessageSerializerList(serializers.ModelSerializer):
    """
    Serializer class for AppMessages
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = AppMessage
        fields = ['id', 'owner', 'subject', 'sent']


class AppMessageSerializer(serializers.ModelSerializer):
    """
    Serializer class for AppMessages
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = AppMessage
        fields = '__all__'


class AppMessageDetailSerializer(serializers.ModelSerializer):
    """
    Serializer class for AppMessages
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    reciver = serializers.ReadOnlyField(source='reciver.username')

    class Meta:
        model = AppMessage
        fields = '__all__'
