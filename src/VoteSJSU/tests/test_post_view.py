from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import json


class PostTestCase(TestCase):
    title = 'test'
    post_type = 'poll'

    def test_post_endpoint(self):
        client = APIClient()
        post_response = client.post(
            '/post/',
            {
                'title': self.title,
                'type': self.post_type,
            },
            format='json'
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED, 'Failed to create new post')
        post_content = json.JSONDecoder().decode(post_response.content.decode())
        get_response = client.get('/post/?id=' + str(post_content['post_id']))
        self.assertEqual(get_response.status_code, status.HTTP_200_OK, 'Failed to retrieve new post')
        get_content = json.JSONDecoder().decode(get_response.content.decode())[0]
        self.assertEqual(get_content['title'], self.title, 'Response data did not match posted data')

    def test_get_all(self):
        client = APIClient()
        get_response = client.get('/post/')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK, 'Failed to get all posts')

    def test_delete_post(self):
        client = APIClient()
        post_response = client.post(
            '/post/',
            {
                'title': self.title,
                'type': self.post_type,
            },
            format='json'
        )
        post_content = json.JSONDecoder().decode(post_response.content.decode())
        delete_response = client.delete('/post/?id=' + str(post_content['post_id']))
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT, 'Failed to delete post')
