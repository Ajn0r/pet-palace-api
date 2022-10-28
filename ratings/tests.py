from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Rating
from pet_sittings.models import PetSitting
from pets.models import Pet


class RatingListTest(APITestCase):
    """
    Class to test the list and create
    view for the rating model
    """
    def setUp(self):
        ere = User.objects.create_user(username='ere', password='pass')
        dere = User.objects.create_user(username='dere', password='pass')
        petsitting = PetSitting.objects.create(
                owner=ere, petsitter=dere,
                compensation='400', location='Stockholm',
                date_from='2023-01-20', date_to='2023-01-24',
                description='A pet-sitting'
        )
        kitty = Pet.objects.create(
                owner=ere, date_of_birth='2020-02-20', name='Kitty'
        )
        petsitting.pets.set([kitty])

    def test_user_can_view_ratings(self):
        ere = User.objects.get(username='ere')
        petsitting = PetSitting.objects.get(owner=ere)
        rating = Rating.objects.create(
            owner=ere, rate=3, petsitting=petsitting,
            comment='Alright petsitting')
        response = self.client.get('/ratings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_rating(self):
        ere = self.client.login(username='ere', password='pass')
        petsitting = PetSitting.objects.get(owner=ere).id
        response = self.client.post('/ratings/', {
            'rate': 4, 'petsitting': petsitting
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rate'], 4)

    def test_loggedin_user_can_only_create_one_rating_for_one_petsitting(self):
        ere = self.client.login(username='ere', password='pass')
        petsitting = PetSitting.objects.get(owner=ere).id
        response1 = self.client.post('/ratings/', {
            'rate': 4, 'petsitting': petsitting
        })
        response2 = self.client.post('/ratings/', {
            'rate': 2, 'petsitting': petsitting
        })
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response1.data['rate'], 4)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_only_create_if_they_are_petsitting_owner(self):
        dere = self.client.login(username='dere', password='pass')
        ere = User.objects.get(username='ere')
        petsitting = PetSitting.objects.get(owner=ere).id
        response = self.client.post('/ratings/', {
            'rate': 4, 'petsitting': petsitting
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
