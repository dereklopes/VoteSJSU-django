from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from VoteSJSU.models import Account, Post, Comment
import json


class CommentTestCase(TestCase):
    test_post = None
    test_post_title = 'test'
    test_post_type = 'poll'
    test_author = None
    test_author_email = 'test@sjsu.edu'

    @classmethod
    def setUpClass(cls):
        # Create new account
        cls.test_author = Account.objects.create(email=cls.test_author_email, name='John Test')
        # Create new post
        cls.test_post = Post.objects.create(
            title=cls.test_post_title, post_type=cls.test_post_type, author=cls.test_author
        )

    def test_comment_endpoint(self):
        client = APIClient(enforce_csrf_checks=False)
        # POST
        post_response = client.post(
            '/post/comment/',
            {
                'post': self.test_post.post_id,
                'author': self.test_author_email,
                'content': 'test comment',
            },
            format='json'
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED, 'Failed to create new comment')
        post_content = json.JSONDecoder().decode(post_response.content.decode())

        # GET Comment
        get_response = client.get('/post/comment/?comment_id=' + str(post_content['comment_id']))
        self.assertEqual(get_response.status_code, status.HTTP_200_OK, 'Failed to retrieve new comment')
        get_content = json.JSONDecoder().decode(get_response.content.decode())[0]
        self.assertEqual(get_content['post'], self.test_post.post_id, 'Response data did not match posted data')

        # DELETE
        delete_response = client.delete('/post/comment/?id=' + str(post_content['comment_id']))
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT, 'Failed to delete comment')


    @classmethod
    def tearDownClass(cls):
        cls.test_post.delete()
        cls.test_author.delete()
