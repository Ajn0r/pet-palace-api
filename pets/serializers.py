from django.db import IntegrityError
from datetime import date
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
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    is_owner = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def validate_image(self, value):
        """
        Function to handle image validation
        """
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'The size of the image cannot be larger than 2MB'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'The width of the image cannot be more than 4069px'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'The height of the image cannot be more than 4069px'
            )
        return value

    def get_age(self, obj):
        """
        Function to get the pets age
        Code inspired by Danny W. Adair code from
        stackoverflow, credits in the readme.
        """
        today = date.today()
        dob = obj.date_of_birth
        years = today.year - dob.year - (
            (today.month, today.day) < (dob.month, dob.day))
        months = today.month - dob.month
        days = today.day - dob.day
        if (today.month < dob.month):
            return f"{years} Years, {12+months} months"
        elif (months == 0 and years <= 0):
            return f"{days} Days"
        else:
            return f"{years} Years, {months} months"

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })

    class Meta:
        """
        Meta class for pet serializer
        """
        model = Pet
        fields = [
            'id', 'owner', 'name', 'description', 'image', 'type',
            'created_at', 'updated_at', 'is_owner', 'date_of_birth',
            'age', 'profile_id', 'get_type_display'
        ]
