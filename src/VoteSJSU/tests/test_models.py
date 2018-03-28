from django.test import TestCase
from VoteSJSU.models import *


class ModuleTestCase(TestCase):
    def test_post_model(self):
        # Set up test data
        title = 'Tests Post'
        account = Account(email='test@test.com', name='John Doe')
        account.save()
        post_type = 'poll'
        url = 'test.com'
        # Create and save the post model
        post = Post(title=title, author=account, post_type=post_type, url=url)
        post.save()
        # Verify the data was saved correctly
        self.assertEqual(1, len(Post.objects.filter(title__exact=title)))
        self.assertEqual(1, len(Post.objects.filter(author__exact=account)))
        self.assertEqual(1, len(Post.objects.filter(post_type__exact=post_type)))
        self.assertEqual(1, len(Post.objects.filter(url__exact=url)))
        # Clean up
        post.delete()
        account.delete()

    def test_account_model(self):
        # Set up test data
        email = 'test@tests.com'
        name = 'John Doe'
        # Create and save the account model
        account = Account(email=email, name=name)
        account.save()
        # Verify the data was saved correctly
        self.assertEqual(1, len(Account.objects.filter(email__exact=email)))
        self.assertEqual(1, len(Account.objects.filter(name__exact=name)))
        # Clean up
        account.delete()
