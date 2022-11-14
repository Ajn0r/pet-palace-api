from django.db import models
from django.contrib.auth.models import User
from pets.models import Pet


class PetChoice(models.Model):
    """
    Choices for pets for the Ad model
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Ad(models.Model):
    """
    Ad model class, for pet-sitting
    ads, a user can connect one or
    many of their pets to the ad.
    If no pets added it is a ad for
    pet-sitters offering pet-sittings.
    """
    STATUS_CHOISES = [
        (0, 'Draft'), (1, 'Active'), (2, 'Finished')
    ]
    TYPE_CHOISES = [
        (0, 'Pet-sitting'), (1, 'Pet-sitter'), (2, 'Unspecified')
    ]
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ad_owner')
    pets = models.ManyToManyField(PetChoice, related_name='ad', blank=True)
    type = models.SmallIntegerField(choices=TYPE_CHOISES, default=2)
    title = models.CharField(max_length=70)
    description = models.TextField()
    image = models.ImageField(
        upload_to='images/', blank=True
    )
    date_from = models.DateField()
    date_to = models.DateField()
    compensation = models.CharField(max_length=130)
    location = models.CharField(max_length=150)
    status = models.SmallIntegerField(choices=STATUS_CHOISES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_from', '-created_at']

    def __str__(self):
        return f"{self.owner}'s ad {self.title}"
