from django import forms
from customer.models import Client, Domain

class CustomerForm(forms.ModelForm):

	class Meta:
		model = Client
		fields = (
			'name',
			'short',
			'contact_fisrt_name',
			'contact_last_name',
			'contact_email',
			'contact_phone',
			'country',
			'school_size',
		)