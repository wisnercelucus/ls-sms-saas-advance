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

#from rest_framework.views import APIView
#from rest_framework.response import Response


#class LikeToggleAPIView(APIView):
#    permission_classes = [permissions.IsAuthenticated]
#    def get(self, request, pk, format=None):
#       post_qs = Post.objects.filter(pk=pk)
#       message = "Not allowed"
#       if request.user.is_authenticated:
#            is_liked, likes = Post.objects.like_toggle(request.user, post_qs.first())
#            return Response({'liked': is_liked, 'likes':likes})
#       return Response({"message": message}, status=400)





class CommentCreateApiView(generics.CreateAPIView):
	permission_classes = [permissions.IsAuthenticated]
	queryset = Comment.objects.all()

	def get_serializer_class(self):
		model_type = self.request.GET.get('type')
		pk =  self.request.GET.get('pk')
		parent_id = self.request.GET.get('parent_id', None)
		return comment_create_serializer(
			model_type=model_type, pk=pk, parent_id=parent_id, 
			user=self.request.user)
	
	#def perform_create(self, serializer):
	#	serializer.save(user=self.request.user)

class CommentDetailApiView(generics.RetrieveAPIView):

	serializer_class = CommentDetailSerializer
	permission_classes = [permissions.IsAuthenticated]
	queryset = Comment.objects.all()


class CommentListApiView(generics.ListAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = CommentModelSerializer
	#pagination_class = StandardCommentResultPagination

	def get_serializer_context(self, *args, **kwargs):
		context = super(CommentListApiView, self).get_serializer_context(*args, **kwargs)
		context['request'] = self.request
		return context

	def get_queryset(self, *args, **kwargs):
		#requested_user = self.kwargs.get("username")
		#print(requested_user)
		qs = None
		#if requested_user:
		qs = Comment.objects.all()
		return qs
