from rest_framework import serializers
from .models import Rating
from pet_sittings.models import PetSitting


class PetSitChoisePKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        queryset = PetSitting.objects.filter(owner=user)
        return queryset


class RatingSerializer(serializers.ModelSerializer):
    rate_choise = [1, 2, 3, 4, 5]
    owner = serializers.ReadOnlyField(source='owner.username')
    petsitting = PetSitChoisePKField()
    rate = serializers.ChoiceField(choices=rate_choise)

    class Meta:
        model = Rating
        fields = '__all__'
