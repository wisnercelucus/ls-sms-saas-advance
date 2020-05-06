from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
	message="Must be the owner of the record to perform this action."
	def has_object_permission(self, request, view, obj):
		return obj.user == request.user
