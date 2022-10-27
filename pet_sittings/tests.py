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
            date_from='2023-01-20', date_to='2023-01-24',
            description='A pet-sitting'
        )
        kitty = Pet.objects.create(
            owner=ere, date_of_birth='2020-02-20', name='Kitty'
        )
        petsitting.pets.set([kitty])

    def test_petsittings_list(self):
        response = self.client.get('/petsittings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_petsitting(self):
        ere = self.client.login(username='ere', password='pass')
        dere = User.objects.get(username='dere').id
        kitty = Pet.objects.get(name='Kitty', owner=ere).id
        response = self.client.post('/petsittings/', {
            'petsitter': dere, 'compensation': '100kr',
            'location': 'stockholm', 'date_from': '2023-01-20',
            'date_to': '2023-01-24', 'pets': kitty,
            'description': 'A pet-sitting'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['pets'], [1])

    def test_owner_can_only_choose_from_own_pets(self):
        ere = self.client.login(username='ere', password='pass')
        dere = User.objects.get(username='dere')
        kitty = Pet.objects.create(
            name='Kitty', owner=dere, date_of_birth='2018-10-14')
        response = self.client.post('/petsittings/', {
            'petsitter': dere, 'compensation': '100kr',
            'location': 'stockholm', 'date_from': '2023-01-20',
            'date_to': '2023-01-24', 'pets': kitty,
            'description': 'A pet-sitting'
        })
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PetSittingDetailTest(APITestCase):
    """
    Class for testing the view
    for viewing detailed petsittings,
    updating and deleting petsittings.
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

    def test_retrive_petsitting_with_id(self):
        response = self.client.get('/petsittings/1')
        self.assertEqual(response.data['compensation'], '400')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_retrive_petsitting_with_invalid_id(self):
        response = self.client.get('/petsittings/966')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_update_petsitting(self):
        self.client.login(username='ere', password='pass')
        response = self.client.patch(
            '/petsittings/1', {'compensation': '450kr'})
        petsitting = PetSitting.objects.filter(pk=1).first()
        self.assertEqual(petsitting.compensation, '450kr')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_others_cannot_update_petsitting(self):
        self.client.login(username='dere', password='pass')
        response = self.client.patch(
            '/petsittings/1', {'compensation': '450kr'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_delete_petsitting(self):
        self.client.login(username='ere', password='pass')
        response = self.client.delete('/petsittings/1')
        count = PetSitting.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_delete_other_users_petsitting(self):
        self.client.login(username='dere', password='pass')
        response = self.client.delete('/petsittings/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
