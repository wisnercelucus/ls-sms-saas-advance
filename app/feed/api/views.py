from feed.models import Post
from .serializers import PostModelSerializer
from rest_framework import mixins
from rest_framework import generics
from django.db.models import Q
from rest_framework import permissions
from .pagination import StandardPostResultPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly


class LikeToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk, format=None):
       post_qs = Post.objects.filter(pk=pk)
       message = "Not allowed"
       if request.user.is_authenticated:
            is_liked, likes = Post.objects.like_toggle(request.user, post_qs.first())
            return Response({'liked': is_liked, 'likes':likes})
       return Response({"message": message}, status=400)


class PostShareApiView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request, pk, format=None):
		post_ps = Post.objects.filter(pk=pk)
		if post_ps.exists() and post_ps.count() == 1:
			if request.user.is_authenticated:
				new_post = Post.objects.share(request.user, post_ps.first())
				data = PostModelSerializer(new_post).data
				return Response(data)
		return Response(None, status=400)

class PostCreateApiView(generics.CreateAPIView):
	serializer_class = PostModelSerializer
	permission_classes = [permissions.IsAuthenticated]
	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class PostUpdateApiView(generics.UpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostModelSerializer
	permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]



class PostDetailApiView(generics.RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostModelSerializer
	permission_classes = [permissions.IsAuthenticated]


class PostDeleteApiView(generics.DestroyAPIView):
	serializer_class = PostModelSerializer
	permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

	def get_queryset(self):
		queryset = Post.objects.filter(pk=self.kwargs['pk'])
		return queryset

	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		if not instance:
			return Response("Cannot delete null object", status=status.HTTP_400_BAD_REQUEST)
		self.perform_destroy(instance)


class PostListApiView(generics.ListAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = PostModelSerializer
	pagination_class = StandardPostResultPagination

	def get_serializer_context(self, *args, **kwargs):
		context = super(PostListApiView, self).get_serializer_context(*args, **kwargs)
		context['request'] = self.request
		return context

	def get_queryset(self, *args, **kwargs):
		requested_user = self.kwargs.get("username")
		if requested_user:
			qs = Post.objects.filter(user__username=requested_user)
		else:
			in_following = self.request.user.profile.get_following()
			qs1 = Post.objects.filter(user__in=in_following)
			qs2 = Post.objects.filter(user=self.request.user)
			qs = (qs1 | qs2).distinct().order_by("-created_at")

		query = self.request.GET.get("q", None)
		if query is not None:
			qs = qs.filter(
				Q(content__icontains=query) |
				Q(user__username__icontains=query)
				)
		return qs
