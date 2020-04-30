from django.db import models
#from tenant_users.tenants.models import TenantBase
from django_countries.fields import CountryField
from django_tenants.models import TenantMixin, DomainMixin

SCHOOL_SIZE = (
	('small',  'less than 100 students'),
	('medium', '101 to 500 students'),
	('wide',   '501 to 1000 students'),
	('extra wide', '1001+ students'),
	)

class Client(TenantMixin):
	name               = models.CharField(max_length=255)
	short              = models.CharField(max_length=50, null=True, blank=True)
	contact_email 	   = models.CharField(max_length=255)
	contact_fisrt_name = models.CharField(max_length=255)
	contact_last_name  = models.CharField(max_length=255)
	contact_phone      = models.IntegerField()
	country            = CountryField()
	school_size 	   = models.CharField(choices=SCHOOL_SIZE, max_length=255)
	paid_until         = models.DateField(null=True)
	on_trial           = models.BooleanField(null=True)
	created_on         = models.DateField(auto_now_add=True)

class Domain(DomainMixin):
	pass
