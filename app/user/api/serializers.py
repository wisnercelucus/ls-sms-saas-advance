from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _


User = get_user_model()

class UserModelSerializer(serializers.ModelSerializer):
	url = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
			'url',
			'image',
		]

	def get_url(self, obj):
		return reverse_lazy("user:profile", kwargs={"username": obj.username})


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs