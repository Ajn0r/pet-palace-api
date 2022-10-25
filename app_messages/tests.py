from django.contrib.auth.models import User
from django.db.models import Q
from .models import AppMessage
from rest_framework import status
from rest_framework.test import APITestCase


class AppMessageListTest(APITestCase):
    """
    Class to test the view for
    listing all messages that belongs to
    owner and revicer
    """
    def setUp(self):
        ere = User.objects.create_user(username='ere', password='pass')
        dere = User.objects.create_user(username='dere', password='pass')
        dure = User.objects.create_user(username='dure', password='pass')
        AppMessage.objects.create(
            owner=ere, reciver=dere, subject='Message',
            content='My first message')

    def test_user_can_view_message_list_if_logged_in(self):
        self.client.login(username='dere', password='pass')
        response = self.client.get('/messages/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_view_others_message_list_if_logged_in(self):
        """
        Test to make sure users cannot see other
        peoples messages, but still getting a 200
        response when viewing the list og messages.
        """
        self.client.login(username='dure', password='pass')
        dure = User.objects.get(username='dure')
        response = self.client.get('/messages/')
        message = AppMessage.objects.all().filter(
            Q(owner=dure) | Q(reciver=dure)
            ).count()
        self.assertEqual(message, 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AppMessageCreateTest(APITestCase):
    """
    Testing the creating view of
    AppMessage.
    """
    def setUp(self):
        User.objects.create_user(username='ere', password='pass')
        User.objects.create_user(username='dere', password='pass')
        User.objects.create_user(username='dure', password='pass')

    def test_can_send_message_if_logged_in(self):
        dere = User.objects.get(username='dere').pk
        self.client.login(username='ere', password='pass')
        url = ('/messages/new')
        data = {
            'reciver': dere,
            'subject': 'Hello!',
            'content': 'Hello dere, how are you?',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_correct_users_are_connected_to_message(self):
        dere = User.objects.get(username='dere').pk
        self.client.login(username='ere', password='pass')
        url = ('/messages/new')
        data = {
            'reciver': dere,
            'subject': 'Hello!',
            'content': 'Hello dere, how are you?',
        }
        response = self.client.post(url, data)
        message = AppMessage.objects.get(pk=1)
        self.assertEqual(message.owner.username, 'ere')
        self.assertEqual(message.reciver.username, 'dere')


class AppMessageDetailTest(APITestCase):
    """
    Test class for the app message
    detail view.
    """
    def setUp(self):
        ere = User.objects.create_user(username='ere', password='pass')
        dere = User.objects.create_user(username='dere', password='pass')
        dure = User.objects.create_user(username='dure', password='pass')
        AppMessage.objects.create(
            owner=ere, reciver=dere, subject='Message',
            content='My first message')

    def test_user_cannot_view_message_if_not_logged_in(self):
        response = self.client.get('/messages/1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_view_others_message_detail_if_logged_in(self):
        self.client.login(username='dure', password='pass')
        response = self.client.get('/messages/1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_message_owner_can_delete_message(self):
        self.client.login(username='ere', password='pass')
        response = self.client.delete('/messages/1')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_message_reciver_cannot_delete_message(self):
        self.client.login(username='dere', password='pass')
        response = self.client.delete('/messages/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
