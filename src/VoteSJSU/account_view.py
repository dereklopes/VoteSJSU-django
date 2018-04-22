from rest_framework.views import APIView
from oauth2client import client, crypt
from django.http.response import JsonResponse, HttpResponse
from rest_framework import status
from VoteSJSU.models import Account
from VoteSJSU.serializers import AccountSerializer


class AccountView(APIView):
    def post(self, request, *args, **kwargs):
        token = self.request.data['token']
        user_id = self.request.data['userId']
        email = self.request.data['email']

        if not self.verify_sjsu_email(email):
            return HttpResponse('Not an SJSU email', status=status.HTTP_400_BAD_REQUEST)

        account = None
        try:
            # attempt to get the account object
            Account.objects.get(email__exact=email)
        except Account.DoesNotExist:
            # account doesn't exist, create a new one

            account = AccountSerializer(data=self.request.data)
            if account.is_valid():
                account.save()
            else:
                return JsonResponse(account.errors, status=status.HTTP_400_BAD_REQUEST)

        if token == 'ACCOUNTTESTTOKEN':
            # this is a test, do not verify token
            return HttpResponse(status=status.HTTP_200_OK)

        if user_id and token:
            try:
                idinfo = client.verify_id_token(token, user_id)
                return JsonResponse(data=idinfo, status=status.HTTP_200_OK)
            except crypt.AppIdentityError:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse(status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        account_queryset = Account.objects.filter(email__exact=self.request.query_params.get('email'))
        serializer = AccountSerializer(account_queryset, many=True)
        return JsonResponse(data=serializer.data, status=status.HTTP_200_OK, safe=False)

    def verify_sjsu_email(self, email: str):
        """
        Verify an email is an SJSU email
        :param email: the email to verify
        :return: boolean, true if SJSU email
        """
        try:
            domain = email.split('@')[1]
            if domain.lower() == 'sjsu.edu':
                return True
            return False
        except IndexError:
            # not an email address
            return False
