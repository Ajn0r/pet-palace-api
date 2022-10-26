from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import PetSitting, Pet


class PetSittingTest(APITestCase):
    """
    Class for testing the view
    for listing and creating
    petsittings.
    """
    def setUp(self):
        ere = User.objects.create_user(username='ere', password='pass')
        dere = User.objects.create_user(username='dere', password='pass')
        petsitting = PetSitting.objects.create(
            owner=ere, petsitter=dere,
            compensation='400', location='Stockholm',
            date_from='2023-01-20', date_to='2023-01-24'
        )
        kitty = Pet.objects.create(
            owner=ere, date_of_birth='2020-02-20', name='Kitty'
        )
        petsitting.pets.set([kitty])

    def test_petsittings_list(self):
        response = self.client.get('/petsittings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

