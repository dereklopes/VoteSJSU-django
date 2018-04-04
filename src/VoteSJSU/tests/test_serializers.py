from django.test import TestCase
from VoteSJSU.serializers import *
from VoteSJSU.models import Post, Account


class SerializerTestCase(TestCase):
    post_title = 'test title'
    author_email = 'test@test.com'
    author_name = 'test'
    author = None
    post = None

    @classmethod
    def setUpTestData(cls):
        cls.author = Account(email=cls.author_email, name=cls.author_name)
        cls.author.save()
        cls.post = Post(title=cls.post_title, author=cls.author)
        cls.post.save()

    def test_post_serializer(self):
        serializer = PostSerializer(self.post)
        self.assertEqual(self.post_title, serializer.data.get('title'))
        self.assertEqual(self.author_email, serializer.data.get('author'))

    def test_account_serializer(self):
        serializer = AccountSerializer(self.author)
        self.assertEqual(self.author_name, serializer.data.get('name'))
        self.assertEqual(self.author_email, serializer.data.get('email'))

    @classmethod
    def tearDownClass(cls):
        cls.author.delete()
        cls.post.delete()
