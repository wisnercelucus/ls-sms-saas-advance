from django.shortcuts import render, redirect
from django.urls import reverse
import os
import stripe
stripe.api_key = os.environ.get("STRIPE_KEY")


def index(request):
	print("Key is: ", os.environ.get('STRIPE_KEY'))
	return render(request, 'donate/donate.html')


def charge_carte(request):

    if request.method == 'POST':
        print('Data: ', request.POST)
        message = None
        context={}
        if request.POST['select_amount'] == 'custom':
        	custom_amount = request.POST['custom_amount']
        	try:
        		custom_amount = int(float(custom_amount))
        	except:
        		message ="Oopps, the custum amount is not number"
        		context['message_custom'] = message
        		return render(request, 'donate/donate.html', context)
        	if custom_amount < 0:
        		message ="Opps, it looks like you have provided a negative donation, we can't process it."
        		context['message_custom'] = message
        		return render(request, 'donate/donate.html', context)
        	amount = custom_amount
        else:
        	select_amount = request.POST['select_amount']
        	try:
        		select_amount = int(float(select_amount))
        	except:
        		message ="Oopps, the selected amount is not number."
        		context['message_select'] = message
        		return render(request, 'donate/donate.html', context)
        	if select_amount < 0:
        		message = "Opps, it looks like you have provided a negative donation, we can't process it."
        		context['message_select'] = message
        		return render(request, 'donate/donate.html', context)
        	amount = select_amount

        customer = stripe.Customer.create(
        	email=request.POST['email'],
        	name=request.POST['name'],
        	source=request.POST['stripeToken']
        	)

        stripe.Charge.create(
        	customer=customer,
        	amount= int(amount) * 100,
        	currency="usd",
        	description="Donation"
        	)

    return redirect(reverse('donate:thank-you', args=[amount]))

def thank_you(request, args):
    amount = args
    context = {'amount': amount}
    return render(request, 'donate/post_donation.html', context)
