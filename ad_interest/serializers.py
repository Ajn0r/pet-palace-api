from django.db import IntegrityError
from rest_framework import serializers
from .models import AdInterest


class AdInterestSerializer(serializers.ModelSerializer):
    """
    Serializer class for ad interest
    from the Code Institute
    django rest walkthrough project
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })

    class Meta:
        model = AdInterest
        fields = ['id', 'owner', 'is_owner', 'ad', 'created_at']
