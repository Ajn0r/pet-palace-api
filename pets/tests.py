from django.contrib.auth.models import User
from .models import Pet
from rest_framework import status
from rest_framework.test import APITestCase


class PetListTest(APITestCase):
    """
    Test class for PetList view, testing that
    logged-in users can view and create pets.
    Also testing restrictions in duplicate pets
    The test code is inspired by the
    Code Institutedjango rest framework
    walkthrough.
    """
    def setUp(self):
        ere = User.objects.create_user(username='ere', password='pass')
        Pet.objects.create(owner=ere, name='kitty', date_of_birth='2021-03-02')

    def test_pet_list(self):
        ere = User.objects.get(username='ere')
        Pet.objects.create(owner=ere, name='Kitty', date_of_birth='2012-01-20')
        response = self.client.get('/pets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_pet(self):
        self.client.login(username='ere', password='pass')
        response = self.client.post(
            '/pets/', {'name': 'kitty', 'date_of_birth': '2021-03-05'})
        self.assertEqual(Pet.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_in_user_cannot_create_duplicate_pet(self):
        self.client.login(username='ere', password='pass')
        response = self.client.post(
            '/pets/', {'name': 'kitty', 'date_of_birth': '2021-03-02'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
