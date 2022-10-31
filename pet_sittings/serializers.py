from django.contrib.auth.models import User
from rest_framework import serializers
from .models import PetSitting
from pets.models import Pet


class PetToSitPKField(serializers.PrimaryKeyRelatedField):
    """
    To only allow the owner to choose from
    the pets that belong to them, code from
    Xavier Ordoquy on medium.com, link can
    be found in readme under credits.
    """
    def get_queryset(self):
        user = self.context['request'].user
        queryset = Pet.objects.filter(owner=user).exclude(owner__is_staff=True)
        return queryset


class PetSitterPKField(serializers.PrimaryKeyRelatedField):
    """
    To only allow user to choose petsitter
    that is not self or that has 'is_staff'
    status. Inspired by the code above.
    """
    def get_queryset(self):
        user = self.context['request'].user
        queryset = User.objects.all().exclude(
            is_staff=True).exclude(
                username=user.username).order_by('followed')
        return queryset


class PetSittingSerializer(serializers.ModelSerializer):
    """
    Serializer class for petsittings, solution
    on how to limit data choises for pets is
    from Xavier Ordoquy on medium.com, link can
    be found in readme under credits.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    pets = PetToSitPKField(many=True)
    petsitter = PetSitterPKField()
    is_petsitter = serializers.SerializerMethodField()
    nr_of_pets_to_sit = serializers.ReadOnlyField()
    date_from = serializers.DateField()
    date_to = serializers.DateField()

    def validate(self, data):
        """
        Check that date_from is before date_to.
        """
        if data['date_from'] > data['date_to']:
            raise serializers.ValidationError(
                "The end date must be before the start date")
        return data

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
            'created_at', 'updated_at', 'is_petsitter', 'nr_of_pets_to_sit'
        ]
