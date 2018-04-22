from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from VoteSJSU.models import Account
import json


class AccountTestCase(TestCase):
    email = 'test@sjsu.edu'
    name = 'John Test'
    token = 'ACCOUNTTESTTOKEN'
    user_id = 'test'

    def test_account_create(self):
        client = APIClient()
        post_response = client.post(
            '/account/',
            {'email': self.email, 'name': self.name, 'token': self.token, 'userId': 'test'},
            format='json'
        )
        self.assertEqual(post_response.status_code, status.HTTP_200_OK)

        # check to see if the account was created
        try:
            account = Account.objects.get(email__exact=self.email)
            self.assertEqual(account.email, self.email, 'Account email does not match posted email')
            self.assertEqual(account.name, self.name, 'Account name does not match posted name')
            # clean up
            account.delete()
        except Account.DoesNotExist:
            self.fail('Account was not created')

    def test_deny_non_sjsu(self):
        client = APIClient()
        email = 'test@gmail.com'
        post_response = client.post(
            '/account/',
            {'email': email, 'name': self.name, 'token': self.token, 'userId': 'test'},
            format='json'
        )
        self.assertEqual(post_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaises(Account.DoesNotExist, Account.objects.get, email__exact=email)

    def test_get_account(self):
        account = Account.objects.create(email=self.email, name=self.name)
        client = APIClient()
        get_response = client.get('/account/?email=' + self.email)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK, 'Got bad return code from /account/ GET')
        response_json = json.JSONDecoder().decode(get_response.content.decode())[0]
        self.assertEqual(response_json['email'], self.email, 'Email retrieved is not correct')
        self.assertIsNotNone(response_json['points'], 'Account points not returned by GET')
        account.delete()
