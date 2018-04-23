from VoteSJSU.serializers import CommentSerializer
from VoteSJSU.models import Comment
from django.db.models import QuerySet
from rest_framework.views import APIView
from django.http.response import JsonResponse, HttpResponse
from rest_framework import status


class CommentView(APIView):
    def get_queryset(self):
        filter_id = self.request.query_params.get('id')
        filter_author = self.request.query_params.get('author')
        filter_post = self.request.query_params.get('post')
        filter_content = self.request.query_params.get('content')

        # If ID is provided, get that comment
        if filter_id:
            return Comment.objects.filter(comment_id__exact=comment_id)
        # otherwise build a queryset with all matching comment
        queryset = QuerySet(model=Comment)
        if filter_author:
            queryset.union(Comment.objects.filter(author__exact=filter_author))
        if filter_post:
            queryset.union(Comment.objects.filter(post__exact=filter_post))
        if filter_content:
            queryset.union(Comment.objects.filter(content__exact=filter_content))
        if not queryset:
            return Comment.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CommentSerializer(queryset, many=True)
        return JsonResponse(data=serializer.data, status=status.HTTP_200_OK, safe=False)

    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data=serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            comment = Comment.objects.get(comment_id__exact=self.request.query_params.get('id'))
        except Comment.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
