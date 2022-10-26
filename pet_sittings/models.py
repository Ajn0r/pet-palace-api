from django.db import models
from django.contrib.auth.models import User
from pets.models import Pet


class PetSitting(models.Model):
    """
    Class for Petsitting model
    for creating petsittings between
    two users and the pets.
    """
    STATUS_CHOISES = [
        (0, 'Planned'), (1, 'Ongoing'), (2, 'Finished')
    ]
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sitting_owner')
    petsitter = models.ForeignKey(
        User, on_delete=models.SET('deleted'), related_name='petsitter')
    pets = models.ManyToManyField(Pet, related_name='pets_to_sit', blank=True)
    description = models.TextField()
    compensation = models.CharField(max_length=130)
    date_from = models.DateField()
    date_to = models.DateField()
    location = models.CharField(max_length=150)
    status = models.SmallIntegerField(choices=STATUS_CHOISES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['status', 'date_from', '-created_at']

    def __str__(self):
        return f"{self.owner} petsitting by {self.petsitter}"
