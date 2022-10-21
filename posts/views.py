from django.db.models import Count
from rest_framework import generics, permissions, filters
from .models import Post
from .serializers import PostSerializer
from pet_palace_api.permissions import IsOwnerOrReadOnly


class PostList(generics.ListCreateAPIView):
    """
    Class for viewing posts and creating if logged in.
    inspired by the Code Institute
    django rest walkthrough project
    """
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True),
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    ordering_fields = [
        'comments_count',
        'likes_count',
        'likes__created_at'
    ]
    search_fields = [
        'owner__username',
        'title',
    ]

    def perform_create(self, serializer):
        """
        Creates the post and associates it with the signed in user
        """
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Class for retriving a post to view, edit or delete
    inspired by the Code Institute
    django rest walkthrough project
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
