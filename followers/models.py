from django.db import models
from django.contrib.auth.models import User


class Follower(models.Model):
    """
    Follower model class,
    code is from the Code Institute
    django rest walkthrough project
    with minor alterations
    """
    owner = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        User, related_name='followed', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'followed'], name='following_constraint')
        ]

    def __str__(self):
        return F"{self.owner} {self.followed}"
