from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Post model class
    inspired by the Code Institute
    django rest walkthrough project
    """
    categories_choises = [
        ('pets', 'Pets'), ('petsittings', 'Pet sittings'),
        ('cats', 'Cats'), ('dogs', 'Dogs'), ('birds', 'Birds'),
        ('horses', 'Horses'), ('wildanimals', 'Wild animals'),
        ('exoticanimals', 'Exotic animals'), ('mammals', 'Mammals'),
        ('fish', 'Fish'), ('reptiles', 'Reptiles'), ('insects', 'Insects'),
        ('uncategorized', 'Uncategorized'), ('other', 'Other')
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_post_thbiny',
        blank=True)
    category = models.CharField(
        choices=categories_choises, default='uncategorized',
        max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Class to order the post by date added
        """
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.id} {self.title}"
