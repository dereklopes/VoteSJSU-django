from VoteSJSU.serializers import PostSerializer
from VoteSJSU.models import Post
from django.db.models import QuerySet
from rest_framework.views import APIView
from django.http.response import JsonResponse, HttpResponse
from rest_framework import status


class PostView(APIView):
    def get_queryset(self):
        filter_id = self.request.query_params.get('id')
        filter_title = self.request.query_params.get('title')
        filter_author = self.request.query_params.get('author')
        filter_type = self.request.query_params.get('type')

        # If ID is provided, get that post
        if filter_id:
            return Post.objects.filter(post_id__exact=filter_id)
        # otherwise build a queryset with all matching posts
        queryset = Post.objects.none()
        if filter_title:
            queryset = queryset.union(Post.objects.filter(title__contains=filter_title))
        if filter_author:
            queryset = queryset.union(Post.objects.filter(author__exact=filter_author))
        if filter_type:
            queryset = queryset.union(Post.objects.filter(post_type__exact=filter_type))
        if not filter_id and not filter_title and not filter_author and not filter_type:
            return Post.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)
        return JsonResponse(data=serializer.data, status=status.HTTP_200_OK, safe=False)

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data=serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(post_id__exact=self.request.query_params.get('id'))
        except Post.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
