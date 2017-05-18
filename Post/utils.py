from django.contrib.auth.models import User
#from geopy.geocoders import GQueryError

# Create your views here.


def associate_by_email(**kwargs):
    try:
        email = kwargs['details']['email']
        kwargs['user'] = User.objects.get(email=email)
    except:
        pass
    return kwargs