from django.contrib.auth.models import User
from .models import AppMessage
from rest_framework import status
from rest_framework.test import APITestCase


class AppMessageListTest(APITestCase):
    """
    Class to test the view for
    listing all messages that belongs to
    owner and revicer
    """
