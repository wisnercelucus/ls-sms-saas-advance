from django.shortcuts import render, redirect
from customer.models import Client, Domain
from customer.forms import CustomerForm
from django.utils import timezone
from django.conf import settings

from core.functions import (
		getShortFromName,
		generate_randowm_password,
	 	email_account_info
	 )

from user.models import User
from django_tenants.utils import schema_context

def create_tenant_domain(schema_name, client, site_domain):
	domain = Domain()
	domain.domain = schema_name + site_domain
	domain.tenant = client
	domain.is_primary = True
	domain.save()

def getTenantDomain(schema_name, site_domain):
	return schema_name + site_domain

def create_tenant_superuser(schema_name=None, username=None, email=None, password=None):
	with schema_context(schema_name):
	    user = User.objects.create_superuser(username=username, email=email, password=password)

def registerProspect(request):
	if request.method == 'GET':
		form = CustomerForm()
		context = {'form': form}
		return render(request, 'customer/register.html', context)
	elif request.method == 'POST':
		form = CustomerForm(data = request.POST)
		client = Client()
		domain = Domain()
		if form.is_valid():
			name = form.cleaned_data['name']
			short = form.cleaned_data['short']

			contact_fisrt_name = form.cleaned_data['contact_fisrt_name']
			contact_last_name = form.cleaned_data['contact_last_name']
			contact_email = form.cleaned_data['contact_email']
			contact_phone = form.cleaned_data['contact_phone']
			school_size = form.cleaned_data['school_size']
			country = form.cleaned_data['country']

			client.contact_fisrt_name = contact_fisrt_name
			client.contact_last_name = contact_last_name
			client.contact_email = contact_email
			client.contact_phone = contact_phone
			client.school_size = school_size
			client.country = country

			if short:
				try:
					client.schema_name = short.lower()
				except:
					client.schema_name = getShortFromName(name)
			else:
				client.schema_name = getShortFromName(name)
			client.name = name
			client.short = short
			client.on_trial = True
			client.paid_until =  timezone.now() + timezone.timedelta(days=30)
			client.save()

			create_tenant_domain(client.schema_name, client, settings.MY_DEMO_DOMAIN)

			rand_password = generate_randowm_password(settings.SUPER_USER_PASSORD_LENGTH)
			create_tenant_superuser(
				schema_name=client.schema_name,
				username=contact_fisrt_name,
				email=contact_email,
				password=rand_password					
					)
			message = 'You successfully registered your school. Please tcheck your email for a link to login to your account.'
			context ={'message': message}
			tenant_domain = getTenantDomain(client.schema_name, settings.MY_DEMO_DOMAIN)
			email_account_info(
			        'Registration success',
			        'customer/post_registration_email.html',
			         contact_fisrt_name,
			         tenant_domain,
			         contact_email,
			         rand_password
			    )
			return render(request, 'customer/register_success.html', context)
		else:
			return redirect('')

def registerSuccess(request):
	return render(request, 'customer/register_success.html')
