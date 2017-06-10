from django.shortcuts import render
from mysite import settings
import requests
import json

# Create your views here.

def purchase(request, event_id=-1):
    if event_id != -1:
        username = request.user.username
        user_id = request.user.pk
        r = requests.get('https://wpoppin.com/api/events/{0}'.format(event_id))
        event = r.json()
        event_name = event['title']
        event_address = event['street_address']
        event_city = event['city']
        event_state = event['state']
        event_zip = event['zip_code']
        event_date = event['date']
        event_time = event['time']
        event_price = event['price']
        if event_price == 0:
            return render(request, "templetes/no-result.html")
        
        context = {
                    'event_name':event_name,
                    'event_address':event_address,
                    'event_city':event_city,
                    'event_state':event_state,
                    'event_zip':event_zip,
                    'event_date':event_date,
                    'event_time':event_time,
                    'event_price':event_price
                }

        return render(request, "templates/payment.html", context)
    else:
        return render(request, "templates/no-result.html")

def checkout(request):
    #called by button
    pass
