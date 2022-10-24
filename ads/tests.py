from django.contrib.auth.models import User
from .models import Ad
from rest_framework import status
from rest_framework.test import APITestCase


class AdListTest(APITestCase):
    """
    Test class for AdList view, testing that
    logged-in users can view and create ads.
    The test code is inspired by the
    Code Institutedjango rest framework
    walkthrough.
    """
    def setUp(self):
        ere = User.objects.create_user(username='ere', password='pass')
        Ad.objects.create(
            owner=ere, title='Pet sitter', status=0, pets='C',
            date_from='2012-01-20', date_to='2012-01-24')

    def test_ad_list(self):
        ere = User.objects.get(username='ere')
        Ad.objects.create(
            owner=ere, title='eres ad', description='A ad belonging to ere',
            compensation='100kr', date_from='2022-12-10',
            date_to='2022-12-14', location='Stockholm')
        response = self.client.get('/ads/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_ad(self):
        self.client.login(username='ere', password='pass')
        response = self.client.post(
            '/ads/', {
                'title': 'Kitty watch', 'date_from': '2022-01-20',
                'date_to': '2022-01-24', 'compensation': '100kr',
                'location': 'home', 'description': 'a ad'})
        self.assertEqual(Ad.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AdDetailTest(APITestCase):
    """
    Testing the ad detail view
    The testcode is greatly
    inspired by the Code Institute
    django rest framework walkthough.
    """
    def setUp(self):
        ere = User.objects.create_user(username='ere', password='pass')
        dere = User.objects.create_user(username='dere', password='pass')
        Ad.objects.create(
            owner=ere, title='eres ad', description='A ad belonging to ere',
            compensation='100kr', date_from='2022-12-10',
            date_to='2022-12-14', location='Stockholm'
        )
        Ad.objects.create(
            owner=dere, title='deres ad', description='A ad belonging to dere',
            compensation='150kr', date_from='2022-12-10',
            date_to='2022-12-16', location='Stockholm'
        )

    def test_can_view_ad_detail_with_valid_id(self):
        response = self.client.get('/ads/1')
        self.assertEqual(response.data['title'], 'eres ad')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_view_ad_detail_with_valid_id(self):
        response = self.client.get('/ads/103')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_logged_in_user_can_update_ad(self):
        self.client.login(username='dere', password='pass')
        response = self.client.patch('/ads/2', {'title': 'Dog walking'})
        ad = Ad.objects.filter(pk=2).first()
        self.assertEqual(ad.title, 'Dog walking')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_owner_can_update_ad(self):
        self.client.login(username='ere', password='pass')
        response = self.client.patch('/ads/2', {'title': 'Cat sitting'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_ad(self):
        self.client.login(username='ere', password='pass')
        response = self.client.delete('/ads/1')
        self.assertEqual(Ad.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_only_owner_can_delete_ad(self):
        self.client.login(username='ere', password='pass')
        response = self.client.delete('/ads/2')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
