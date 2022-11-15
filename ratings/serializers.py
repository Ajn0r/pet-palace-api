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
    is_owner = serializers.SerializerMethodField()
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    petsitter_profile_image = serializers.ReadOnlyField(
        source='petsitting.petsitter.profile.image.url')
    petsitting = PetSitChoisePKField()
    rate = serializers.ChoiceField(choices=rate_choise)
    petsitter = serializers.ReadOnlyField(
        source='petsitting.petsitter.username')
    is_petsitter = serializers.SerializerMethodField()
    petsitting_date = serializers.ReadOnlyField(
        source='petsitting.date_from'
    )

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_is_petsitter(self, obj):
        request = self.context['request']
        return request.user == obj.petsitting.petsitter

    class Meta:
        model = Rating
        fields = [
            'id', 'owner', 'is_owner', 'petsitting',
            'rate', 'comment', 'petsitter', 'is_petsitter',
            'created_at', 'updated_at', 'petsitting_date',
            'profile_image', 'petsitter_profile_image',
            ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })
