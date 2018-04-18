from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from VoteSJSU.models import Account, Post
import json


class VoteTestCase(TestCase):
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

    def test_vote_endpoint(self):
        client = APIClient(enforce_csrf_checks=False)
        # POST
        post_response = client.post(
            '/post/vote/',
            {
                'post': self.test_post.post_id,
                'author': self.test_author_email,
                'choice': 4,
            },
            format='json'
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED, 'Failed to create new vote')
        post_content = json.JSONDecoder().decode(post_response.content.decode())

        # GET Vote
        get_response = client.get('/post/vote/?vote_id=' + str(post_content['vote_id']))
        self.assertEqual(get_response.status_code, status.HTTP_200_OK, 'Failed to retrieve new vote')
        get_content = json.JSONDecoder().decode(get_response.content.decode())[0]
        self.assertEqual(get_content['post'], self.test_post.post_id, 'Response data did not match posted data')

        # POST (again for duplicate)
        post_response = client.post(
            '/post/vote/',
            {
                'post': self.test_post.post_id,
                'author': self.test_author_email,
                'choice': 4,
            },
            format='json'
        )
        self.assertNotEqual(post_response.status_code, status.HTTP_201_CREATED, 'Posted duplicate vote')
        self.assertEqual(post_response.status_code, status.HTTP_409_CONFLICT, 'Did not get conflict return code')

        # DELETE
        delete_response = client.delete('/post/vote/?id=' + str(post_content['vote_id']))
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT, 'Failed to delete vote')

    def test_post_updated(self):
        # Get previous votes
        previous_votes = self.test_post.choice2_votes

        # POST new vote
        client = APIClient(enforce_csrf_checks=False)
        post_response = client.post(
            '/post/vote/',
            {
                'post': self.test_post.post_id,
                'author': self.test_author_email,
                'choice': 2,
            },
            format='json'
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED, 'Failed to create new vote')
        post_content = json.JSONDecoder().decode(post_response.content.decode())

        # Check new votes count
        get_response = client.get('/post/?post_id=' + str(post_content['post']))
        self.assertEqual(get_response.status_code, status.HTTP_200_OK, 'Failed to retrieve corresponding post')
        get_content = json.JSONDecoder().decode(get_response.content.decode())[0]
        self.assertEqual(
            get_content['choice2_votes'], previous_votes + 1, 'Votes count on Post model not updated after POST'
        )

        # DELETE new vote
        delete_response = client.delete('/post/vote/?id=' + str(post_content['vote_id']))
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT, 'Failed to delete vote')

        # Check new votes count
        get_response = client.get('/post/?post_id=' + str(post_content['post']))
        self.assertEqual(get_response.status_code, status.HTTP_200_OK, 'Failed to retrieve corresponding post')
        get_content = json.JSONDecoder().decode(get_response.content.decode())[0]
        self.assertEqual(
            get_content['choice2_votes'], previous_votes, 'Votes count on Post model not updated after POST'
        )

    @classmethod
    def tearDownClass(cls):
        cls.test_post.delete()
        cls.test_author.delete()
