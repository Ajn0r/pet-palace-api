from rest_framework import serializers
from .models import AppMessage


class AppMessageSerializer(serializers.ModelSerializer):
    """
    Serializer class for AppMessages
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = AppMessage
        fields = [
            'id', 'owner', 'subject', 'sent'
        ]
