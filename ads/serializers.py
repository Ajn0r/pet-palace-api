from rest_framework import serializers
from .models import Ad


class AdSerializer(serializers.ModelSerializer):
    """
    Serializer class for ads
    """
    owner = serializers.ReadOnlyField(source='ad_owner.username')
    is_owner = serializers.SerializerMethodField()
    pets = serializers.MultipleChoiceField(choices=Ad.PET_CHOISE_AD)

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Ad
        fields = [
            'id', 'owner', 'title', 'description', 'image', 'date_from',
            'date_to', 'compensation', 'location', 'status',
            'created_at', 'updated_at', 'is_owner', 'type', 'pets'
        ]
