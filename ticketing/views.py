from django.shortcuts import render, redirect
from mysite import settings
from .forms import CreditCardForm
import requests
import json
import stripe
import requests.packages.urllib3

# Create your views here.

def purchase(request, event_id=-1):
    if event_id != -1:
        username = request.user.username
        user_id = request.user.pk
        r = requests.get('http://wpoppin.com/api/events/{0}'.format(event_id))
        event = r.json()
        event_name = event['title']
        event_address = event['street_address']
        event_description = event['description']
        event_city = event['city']
        event_state = event['state']
        event_zip = event['zip_code']
        event_date = event['date']
        event_time = event['time']
        event_price = event['price']
        form = CreditCardForm(event_name=event_name, username=username, user_id=user_id, event_price=event_price)
        context = {
                    'event_name':event_name,
                    'event_description':event_description,
                    'event_address':event_address,
                    'event_city':event_city,
                    'event_state':event_state,
                    'event_zip':event_zip,
                    'event_date':event_date,
                    'event_time':event_time,
                    'event_price':event_price,
                    'form':form
                }

        return render(request, "payment.html", context)
    else:
        return render(request, "no-result.html")

def checkout(request):
    if request.method == 'POST':
        try:
            form = request.POST.dict()
            print(form)
            charged, charge_id = stripe_payment(
                    form['exp_month'],
                    form['exp_year'],
                    form['card_number'],
                    form['cvc'],
                    form['name'],
                    form['event_price'])
            print('paid')
            if charged == True:
                confirmation_num = save_purchase(form['event_name'], form['email'], form['username'], form['user_id'], charge_id)
                context = {"confirmation_num":confirmation_num}
                return render(request, 'confirmation.html', context)
            else:
                return render(request, 'error.html')
        except:
            print('form is invalid')
            return render(request, 'error.html')
    else:
        return render(request, 'no-result.html')

def stripe_payment(exp_month, exp_year, number, cvc, name, amount):
    print('got here')
    requests.packages.urllib3.disable_warnings()
    amount = 2
    stripe.api_key = settings.STRIPE_API_KEY
    print(settings.STRIPE_API_KEY)
    try:
        response = stripe.Charge.create(
            amount=int(amount*100),
            currency="usd",
            description="What's Poppin Ticket Purchase",
            card={
                    "exp_month":int(exp_month),
                    "exp_year":int(exp_year),
                    "number":int(number),
                    "cvc":int(cvc),
                    "name":str(name)
                })
    except stripe.CardError, ce:
        return False, ce
    return True, response

def save_purchase(event, email, username, user_id, charge_id):
    json = {
                'event_name':event,
                'email':email,
                'username':username,
                'user_id':user_id,
                'charge_id':charge_id
            }
    r = requests.post('http://wpoppin.com/api/generate_confirmation', json=json)
    return r.json()['confirmation_num']

