from rest_framework import serializers
from .models import Profile
from followers.models import Follower


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer class for profiles
    inspired by the Code Institute
    django rest walkthrough project
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    nr_of_post = serializers.ReadOnlyField()
    following_id = serializers.SerializerMethodField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    nr_of_pets = serializers.ReadOnlyField()
    rating = serializers.ReadOnlyField()
    nr_of_ratings = serializers.ReadOnlyField()
    nr_of_sittings = serializers.ReadOnlyField()
    nr_of_msg_recived = serializers.ReadOnlyField()
    nr_of_msg_sent = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
       
    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'name', 'description', 'image', 'type',
            'created_at', 'updated_at', 'is_owner', 'nr_of_post',
            'following_id', 'followers_count', 'following_count',
            'nr_of_pets', 'rating', 'nr_of_ratings', 'nr_of_sittings',
            'nr_of_msg_recived', 'nr_of_msg_sent'
        ]
