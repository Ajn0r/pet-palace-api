from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import AdInterest
from ads.models import Ad


class AdInterestListTest(APITestCase):
    """
    Test class for testing
    AdInterestList view
    """
    def setUp(self):
        ere = User.objects.create(username='ere', password='pass')
        dere = User.objects.create_user(username='dere', password='pass')
        Ad.objects.create(
            owner=dere, title='deres ad', description='A ad belonging to dere',
            compensation='150kr', date_from='2022-12-10',
            date_to='2022-12-16', location='Stockholm'
        )

    def test_user_can_create_ad_interest(self):
        self.client.login(username='dere', password='pass')
        ad = Ad.objects.get(pk=1).id
        response = self.client.post('/interest/', {'ad': ad})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AdInterestDetailTest(APITestCase):
    """
    Test class for testing
    AdInterestDetail view
    """
    def setUp(self):
        ere = User.objects.create(username='ere', password='pass')
        dere = User.objects.create_user(username='dere', password='pass')
        ad = Ad.objects.create(
            owner=dere, title='deres ad', description='A ad belonging to dere',
            compensation='150kr', date_from='2022-12-10',
            date_to='2022-12-16', location='Stockholm'
        )
        AdInterest.objects.create(owner=dere, ad=ad)

    def test_user_can_delete_ad_interest(self):
        self.client.login(username='dere', password='pass')
        response = self.client.delete('/interest/1')
        self.assertEqual(AdInterest.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_delete_other_users_ad_interest(self):
        self.client.login(username='ere', password='pass')
        response = self.client.delete('/interest/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
