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

    def test_user_can_only_create_rating_if_they_are_petsitting_owner(self):
        dere = self.client.login(username='dere', password='pass')
        ere = User.objects.get(username='ere')
        petsitting = PetSitting.objects.get(owner=ere).id
        response = self.client.post('/ratings/', {
            'rate': 4, 'petsitting': petsitting
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RatingDetailsTest(APITestCase):
    """
    Class to test the retrive, update and
    delete view for the rating model
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
        Rating.objects.create(
            owner=ere, petsitting=petsitting, rate=5,
            comment='Very good petsitting'
        )

    def test_retrive_rating_with_valid_id(self):
        response = self.client.get('/ratings/1')
        self.assertEqual(response.data['rate'], 5)
        self.assertEqual(response.data['comment'], 'Very good petsitting')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_connot_retrive_rating_with_invalid_id(self):
        response = self.client.get('/ratings/101044')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_update_rating(self):
        self.client.login(username='ere', password='pass')
        response = self.client.patch(
            '/ratings/1', {'rate': 4})
        rating = Rating.objects.filter(pk=1).first()
        self.assertEqual(rating.rate, 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_users_can_not_update_rating(self):
        self.client.login(username='dere', password='pass')
        response = self.client.patch(
            '/ratings/1', {'comment': 'The best petsitter ever!!!!'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_delete_rating(self):
        self.client.login(username='ere', password='pass')
        response = self.client.delete('/ratings/1')
        self.assertEqual(Rating.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_other_users_can_not_delete_rating(self):
        self.client.login(username='dere', password='pass')
        response = self.client.delete('/ratings/1')
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
