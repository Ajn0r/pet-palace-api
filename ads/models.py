from django.db import models
from django.contrib.auth.models import User
from pets.models import Pet


class Ad(models.Model):
    """
    Ad model class, for pet-sitting
    ads, a user can connect one or
    many of their pets to the ad.
    If no pets added it is a ad for
    pet-sitters offering pet-sittings.
    """
    STATUS_CHOISES = [
        (0, 'Draft'), (1, 'Active'), (2, 'Ongoing'), (3, 'Finished')
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    pets = models.ManyToManyField(Pet, blank=True)
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
        ordering = ['-date_from', '-created_at']

    def __str__(self):
        return f"{self.owner}'s ad {self.title}"
