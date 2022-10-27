from django.db import models
from django.contrib.auth.models import User
from pet_sittings.models import PetSitting


class Rating(models.Model):
    """
    Rating model class
    """
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='rating_owner')
    rated = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='rating_of_owner')
    petsitting = models.ForeignKey(
        PetSitting, on_delete=models.CASCADE, related_name='petsitting_rating')
    rate = models.PositiveSmallIntegerField()
    comment = models.TextField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        f"{self.owner}'s rating of {self.rated}"
