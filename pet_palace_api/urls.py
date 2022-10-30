"""
pet_palace_api URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path(
        'dj-rest-auth/registration/',
        include('dj_rest_auth.registration.urls')),
    path('', include('profiles.urls')),
    path('', include('posts.urls')),
    path('', include('comments.urls')),
    path('', include('likes.urls')),
    path('', include('followers.urls')),
    path('', include('pets.urls')),
    path('', include('ads.urls')),
    path('', include('app_messages.urls')),
    path('', include('ad_interest.urls')),
    path('', include('pet_sittings.urls')),
    path('', include('ratings.urls')),
]
