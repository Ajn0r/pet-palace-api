from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListTest(APITestCase):
    """
    Testing the postlist view, the testcode is
    greatly inspired by the Code Institute
    django rest framework walkthough.
    """
    def setUp(self):
        User.objects.create_user(username='ene', password='pass')

    def test_list_posts(self):
        ene = User.objects.get(username='ene')
        Post.objects.create(owner=ene, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='ene', password='pass')
        response = self.client.post('/posts/', {'title': 'New title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_only_logged_in_user_can_create_post(self):
        response = self.client.post('/posts/', {'title': 'New title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailTest(APITestCase):
    """
    Testing the post detail view, the testcode is
    greatly inspired by the Code Institute
    django rest framework walkthough.
    """
    def setUp(self):
        ene = User.objects.create_user(username='ene', password='pass')
        dene = User.objects.create_user(username='dene', password='pass')
        Post.objects.create(
            owner=ene, title='Enes title', content='the content of enes post')
        Post.objects.create(
            owner=dene, title='Denes title',
            content='the content of denes post')

    def test_can_retrive_post_with_id(self):
        response = self.client.get('/posts/1')
        self.assertEqual(response.data['title'], 'Enes title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_retrive_post_with_invalid_id(self):
        response = self.client.get('/posts/41')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_post(self):
        self.client.login(username='ene', password='pass')
        response = self.client.put('/posts/1', {'title': 'a new title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_other_users_posts(self):
        self.client.login(username='dene', password='pass')
        response = self.client.put('/posts/1', {'title': 'not my post!'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_post(self):
        self.client.login(username='ene', password='pass')
        response = self.client.delete('/posts/1')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_delete_other_users_post(self):
        self.client.login(username='dene', password='pass')
        response = self.client.delete('/posts/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_default_category_is_uncategorized(self):
        response = self.client.get('/posts/1')
        self.assertEqual(response.data['category'], 'uncategorized')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_default_image_filter_is_normal(self):
        response = self.client.get('/posts/1')
        self.assertEqual(response.data['image_filter'], 'normal')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
