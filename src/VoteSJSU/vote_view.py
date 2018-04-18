from VoteSJSU.serializers import VoteSerializer
from VoteSJSU.models import Post, Vote
from rest_framework.views import APIView
from django.http.response import JsonResponse, HttpResponse
from rest_framework import status


class VoteView(APIView):
    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        vote_id = self.request.query_params.get('vote_id')
        author = self.request.query_params.get('author')

        # if vote_id is provided, return that
        if vote_id:
            return Vote.objects.filter(vote_id__exact=vote_id)
        if post_id and author:
            return Vote.objects.filter(post_id__exact=post_id, author__exact=author)
        elif post_id:
            return Vote.objects.filter(post_id__exact=post_id)
        elif author:
            return Vote.objects.filter(author__exact=author)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = VoteSerializer(queryset, many=True)
        return JsonResponse(data=serializer.data, status=status.HTTP_200_OK, safe=False)

    def post(self, request, *args, **kwargs):
        # Check for existing vote for given post by given author
        try:
            vote = Vote.objects.get(
                post_id__exact=self.request.data['post'],
                author__exact=self.request.data['author']
            )
            # vote already exists, delete it if not duplicate
            if vote.choice == int(self.request.data['choice']):
                return HttpResponse('Duplicate vote', status=status.HTTP_409_CONFLICT)
            vote.delete()
        except Vote.DoesNotExist:
            # create a new vote
            pass
        serializer = VoteSerializer(data=self.request.data)
        if not serializer.is_valid():
            return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        choice = serializer.validated_data['choice']
        post_id = serializer.validated_data['post'].post_id
        serializer.save()

        # Find the corresponding post and update
        if self.update_post_rating_votes(post_id=post_id, choice=choice, amount=1):
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse(data=serializer.data, status=status.HTTP_201_CREATED, safe=False)

    def delete(self, request, *args, **kwargs):
        try:
            vote = Vote.objects.get(vote_id__exact=self.request.query_params.get('id'))
            # Find the corresponding post
        except Vote.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        vote.delete()

        # Update Post object
        if self.update_post_rating_votes(post_id=vote.post_id, choice=vote.choice, amount=-1):
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @classmethod
    def update_post_rating_votes(cls, post_id: int, choice: int, amount: int):
        try:
            post = Post.objects.get(post_id__exact=post_id)
        except Post.DoesNotExist:
            return -1
        # Update Post object
        if post.post_type == 'rating':
            post.num_ratings += amount
            post.rating = post.rating + choice / post.num_ratings
        elif post.post_type == 'poll':
            post.choice1_votes = len(Vote.objects.filter(post_id__exact=post_id, choice__exact=1))
            post.choice2_votes = len(Vote.objects.filter(post_id__exact=post_id, choice__exact=2))
            post.choice3_votes = len(Vote.objects.filter(post_id__exact=post_id, choice__exact=3))
            post.choice4_votes = len(Vote.objects.filter(post_id__exact=post_id, choice__exact=4))
        # Save both post model
        post.save()
        return 0
