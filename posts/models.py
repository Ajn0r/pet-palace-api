from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Post model class
    inspired by the Code Institute
    django rest walkthrough project
    """
    image_filter_choices = [
        ('_1977', '1977'), ('brannan', 'Brannan'),
        ('earlybird', 'Earlybird'), ('hudson', 'Hudson'),
        ('inkwell', 'Inkwell'), ('lofi', 'Lo-Fi'),
        ('kelvin', 'Kelvin'), ('normal', 'Normal'),
        ('nashville', 'Nashville'), ('rise', 'Rise'),
        ('toaster', 'Toaster'), ('valencia', 'Valencia'),
        ('walden', 'Walden'), ('xpro2', 'X-pro II')
    ]
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
    image_filter = models.CharField(
        max_length=32, choices=image_filter_choices, default='normal'
    )
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
