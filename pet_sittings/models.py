from django.db import models
from django.contrib.auth.models import User
from pets.models import Pet


def get_deleted_user():
    """
    Sets the petsitter to deleted if user is
    deleted, so that the petowner's petsittings
    are not deleted.
    """
    deleted_user = User.objects.get(username='Deleted')
    if deleted_user:
        return deleted_user.pk
    raise deleted_user.DoesNotExist('Please add a Deleted User')


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
        User, on_delete=models.CASCADE,
        related_name='sitting_owner'
        )
    petsitter = models.ForeignKey(
        User, on_delete=models.SET(get_deleted_user),
        related_name='petsitter'
        )
    pets = models.ManyToManyField(
        Pet, related_name='pets_to_sit', blank=True
        )
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
        return (
            f"Petsitting by {self.petsitter}, {self.date_from}-{self.date_to}")
