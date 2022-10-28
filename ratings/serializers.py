from django.db import IntegrityError
from rest_framework import serializers
from .models import Rating
from pet_sittings.models import PetSitting


class PetSitChoisePKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        queryset = PetSitting.objects.filter(
            owner=user).filter(status=2).order_by('-date_to')
        return queryset


class RatingSerializer(serializers.ModelSerializer):
    rate_choise = [1, 2, 3, 4, 5]
    owner = serializers.ReadOnlyField(source='owner.username')
    petsitting = PetSitChoisePKField()
    rate = serializers.ChoiceField(choices=rate_choise)

    class Meta:
        model = Rating
        fields = ['id', 'owner', 'petsitting', 'rate', 'comment']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })
