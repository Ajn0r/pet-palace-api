from django.contrib.auth.models import User
from .models import Comment
from posts.models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class CommentListTests(APITestCase):
    """
    Class to test the comment list view
    """
    def setUp(self):
        User.objects.create_user(username='ere', password='pass')

    def test_list_comments(self):
        ere = User.objects.get(username='ere')
        post = Post.objects.create(owner=ere, title='title')
        Comment.objects.create(owner=ere, content='A comment', post=post)
        response = self.client.get('/comments/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CommentDetailTests(APITestCase):
    """
    Class to test comment detail view
    """
    def setUp(self):
        ere = User.objects.create_user(username='ere', password='pass')
        dere = User.objects.create_user(username='dere', password='pass')
        post1 = Post.objects.create(
            owner=ere, title='Eres title', content='Content'
        )
        Comment.objects.create(
            owner=ere, post=post1, content='My comment'
        )
        Comment.objects.create(
            owner=dere, post=post1, content='My other content'
        )

    def test_retriving_comments_with_valid_id(self):
        response = self.client.get('/comments/1')
        self.assertEqual(response.data['content'], 'My comment')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_retriving_comments_with_invalid_id(self):
        response = self.client.get('/comments/1545')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_comment(self):
        self.client.login(username='ere', password='pass')
        response = self.client.put('/comments/1', {'content': 'New content'})
        comment = Comment.objects.filter(pk=1).first()
        self.assertEqual(comment.content, 'New content')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_other_users_comment(self):
        self.client.login(username='dere', password='pass')
        response = self.client.put('/comments/1', {'content': 'New content'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_comment(self):
        self.client.login(username='ere', password='pass')
        response = self.client.delete('/comments/1')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_delete_other_users_comment(self):
        self.client.login(username='dere', password='pass')
        response = self.client.delete('/comments/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
