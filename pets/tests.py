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

    def test_users_pet_count(self):
        ere = User.objects.get(username='ere')
        Pet.objects.create(
            owner=ere, name='kitty', date_of_birth='2020-03-02')
        Pet.objects.create(
            owner=ere, name='kitty', date_of_birth='2019-03-02')
        ere_pets = Pet.objects.filter(owner=ere)
        self.assertEqual(ere_pets.count(), 3)


class PetDetailTest(APITestCase):
    """
    Testing the pet detail view
    The testcode is greatly
    inspired by the Code Institute
    django rest framework walkthough.
    """
    def setUp(self):
        ere = User.objects.create_user(username='ere', password='pass')
        dere = User.objects.create_user(username='dere', password='pass')
        Pet.objects.create(
            owner=ere, name='kitty', date_of_birth='2021-03-02')
        Pet.objects.create(
            owner=dere, name='doggy', date_of_birth='2020-01-20')

    def test_can_view_pet_with_correct_id(self):
        response = self.client.get('/pets/1')
        self.assertEqual(response.data['name'], 'kitty')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_get_pet_with_invalid_id(self):
        response = self.client.get('/pets/253')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_logged_in_user_can_update_own_pet(self):
        self.client.login(username='dere', password='pass')
        response = self.client.patch('/pets/2', {'name': 'doggi'})
        pet = Pet.objects.filter(pk=2).first()
        self.assertEqual(pet.name, 'doggi')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_owner_can_update_pet(self):
        self.client.login(username='ere', password='pass')
        response = self.client.patch('/pets/2', {'name': 'doggo'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_pet(self):
        self.client.login(username='dere', password='pass')
        response = self.client.delete('/pets/2')
        self.assertEqual(Pet.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_default_type_is_other(self):
        response = self.client.get('/pets/1')
        self.assertEqual(response.data['type'], 'other')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
