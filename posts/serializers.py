from rest_framework import serializers
from .models import Post
from likes.models import Like


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer class for posts
    inspired by the Code Institute
    django rest walkthrough project
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()

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

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'title', 'content', 'image', 'image_filter', 'category',
            'created_at', 'updated_at', 'like_id',
        ]
