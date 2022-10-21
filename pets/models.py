from django.db import models
from django.contrib.auth.models import User


class Pet(models.Model):
    """
    Pet model class
    Creates pets that have a connection
    to a user, one user can have many pets
    """
    pet_choises = [
        ('cat', 'Cat'), ('dog', 'Dog'), ('bird', 'Bird'),
        ('horse', 'Horse'), ('wildanimal', 'Wild animal'),
        ('exoticanimal', 'Exotic animal'), ('mammal', 'Mammal'),
        ('fish', 'Fish'), ('reptile', 'Reptile'), ('insecs', 'Insect'),
        ('other', 'Other')

    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    type = models.CharField(
        max_length=50, choices=pet_choises, default='other')
    description = models.TextField(blank=True, max_length=365)
    image = models.ImageField(
        upload_to='images/', default="../petprofile_svixn2"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_of_birth = models.DateField()

    class Meta:
        """
        Meta class for ordering and 
        adding constraint, not allowing a
        owner to have a pet with the same name born
        on the same date.
        """
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'name', 'date_of_birth'],
                name='pet_naming_constraint'
            )
        ]

    def __str__(self):
        return f"{self.owner}'s {self.type}, {self.name}"
