from django.db import models
from django.contrib.auth.models import User
from ads.models import Ad


class AdInterest(models.Model):
    """
    Ad Interest model class
    inspired by the Code Institute
    django rest walkthrough project
    Like model
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(
        Ad, on_delete=models.CASCADE, related_name='interests')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'ad'], name='unique_interest')
        ]

    def __str__(self):
        return f"{self.owner} {self.post}"
