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
    is_owner = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

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
        elif (months == 0):
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
            'age'
        ]
