from django.db import models
from django.db.models.signals import post_save
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
    contact = models.CharField(max_length=90, blank=True, null=True)
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

    def create_profile(sender, instance, created, **kwargs):
        """
        Function to create a profile once a user is created.
        """
        if created:
            Profile.objects.create(owner=instance)

    post_save.connect(create_profile, sender=User)
