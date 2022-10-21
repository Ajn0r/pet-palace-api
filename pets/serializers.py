from rest_framework import serializers
from .models import Pet


class PetSerializer(serializers.ModelSerializer):
    """
    Serializer class for Pets app
    inspired by the Code Institute
    django rest walkthrough project
    with some alteration
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        """
        Meta class for pet serializer
        """
        model = Pet
        fields = [
            'id', 'owner', 'name', 'description', 'image', 'type',
            'created_at', 'updated_at', 'is_owner', 'date_of_birth'
        ]