from django.db import models
from django.contrib.auth.models import User


class AppMessage(models.Model):
    """
    Message model class
    """
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')
    reciver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='message_reciver')
    subject = models.CharField(max_length=90)
    content = models.TextField(blank=True)
    sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent']

    def __str__(self):
        return f"Message from {self.owner} to {self.reciver}"
