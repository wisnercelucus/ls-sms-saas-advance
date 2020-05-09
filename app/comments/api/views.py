from comments.models import Comment
from .serializers import (CommentModelSerializer, 
	CommentDetailSerializer,
	comment_create_serializer,
	)
from rest_framework import mixins
from rest_framework import generics
from django.db.models import Q
from rest_framework import permissions
from .pagination import StandardCommentResultPagination
from .permissions import IsOwnerOrReadOnly
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response


class LikeToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk, format=None):
       comment_qs = Comment.objects.filter(pk=pk)
       message = "Not allowed"
       if request.user.is_authenticated:
            is_liked, likes = Comment.objects.like_toggle(request.user, comment_qs.first())
            return Response({'liked': is_liked, 'likes':likes})
       return Response({"message": message}, status=400)


class CommentCreateApiView(generics.CreateAPIView):
	permission_classes = [permissions.IsAuthenticated]
	queryset = Comment.objects.all()

	def get_serializer_class(self):
		model_type = self.request.POST.get('content_type')
		pk =  self.request.POST.get('object_id')
		parent_id = self.request.POST.get('parent_id', None)

		print('within serializer')

		return comment_create_serializer(
			model_type=model_type, pk=pk, parent_id=parent_id, 
			user=self.request.user)
	
	#def perform_create(self, serializer):

class CommentDetailApiView(generics.RetrieveAPIView):

	serializer_class = CommentDetailSerializer
	permission_classes = [permissions.IsAuthenticated]
	queryset = Comment.objects.filter(id__gte=0)

	def get_serializer_context(self, *args, **kwargs):
		context = super(CommentDetailApiView, self).get_serializer_context(*args, **kwargs)
		context['request'] = self.request
		return context
	

class CommentManagementApiView(UpdateModelMixin, DestroyModelMixin, generics.RetrieveAPIView):

	serializer_class = CommentDetailSerializer
	permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
	queryset = Comment.objects.filter(id__gte=0)

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)


class CommentListApiView(generics.ListAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = CommentModelSerializer
	pagination_class = StandardCommentResultPagination

	def get_serializer_context(self, *args, **kwargs):
		context = super(CommentListApiView, self).get_serializer_context(*args, **kwargs)
		context['request'] = self.request
		return context

	def get_queryset(self, *args, **kwargs):
		qs = None
		qs = Comment.objects.all()
		return qs
