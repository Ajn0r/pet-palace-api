from datetime import date
from rest_framework import serializers
from .models import Ad, PetChoice


class PetChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PetChoice
        fields = '__all__'


def future_date_validation(value):
    """
    Function to make sure that the start date
    is in the future.
    """
    today = date.today()
    if value < today:
        raise serializers.ValidationError(
            "The start date needs to be in the future")
        return value


class AdSerializer(serializers.ModelSerializer):
    """
    Serializer class for ads
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    is_owner = serializers.SerializerMethodField()
    nr_of_interest = serializers.ReadOnlyField()
    date_from = serializers.DateField(validators=[future_date_validation])
    date_to = serializers.DateField()
    contact = serializers.ReadOnlyField(source='owner.profile.contact')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["pets"] = PetChoiceSerializer(instance.pets.all(), many=True).data
        return rep

    def validate_date_to(self, data):
        """
        Check that date_from is before date_to.
        """
        date_from = self.initial_data['date_from']
        date_to = self.initial_data['date_to']
        if date_from > date_to:
            raise serializers.ValidationError(
                "The end date must be after the start date")
        return data

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

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Ad
        fields = [
            'id', 'owner', 'title', 'description', 'image', 'date_from',
            'date_to', 'compensation', 'location', 'status',
            'created_at', 'updated_at', 'is_owner', 'type', 'pets',
            'nr_of_interest', 'profile_id', 'get_status_display',
            'get_type_display', 'profile_image', 'contact'
        ]
