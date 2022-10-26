from rest_framework import serializers
from .models import PetSitting
from pets.models import Pet


class PetSitPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        queryset = Pet.objects.filter(owner=user)
        return queryset


class PetSittingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    pets = PetSitPKField(many=True)
    is_petsitter = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_is_petsitter(self, obj):
        request = self.context['request']
        return request.user == obj.petsitter

    class Meta:
        model = PetSitting
        fields = [
            'id', 'owner', 'petsitter', 'is_owner', 'pets', 'description',
            'date_from', 'date_to', 'compensation', 'location', 'status',
            'created_at', 'updated_at', 'is_petsitter'
        ]
