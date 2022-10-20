from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    User profile model
    inspired by the django rest walkthrough project
    with some added customization
    """
    TYPE_CHOISES = [
        (0, 'Pet friend'),
        (1, 'Pet owner')
    ]

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_ciez4a'
    )
    type = models.IntegerField(choices=TYPE_CHOISES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for ordering profiles
        """
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"
