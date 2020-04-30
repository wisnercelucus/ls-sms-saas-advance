from django.core.exceptions import ValidationError

def validate_field(value):
	field = value
	if field=='':
		raise ValidationError('Cannot be blank')
	return value