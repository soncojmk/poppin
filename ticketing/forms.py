from django import forms
from django.forms.widgets import HiddenInput

class CreditCardForm(forms.Form):
    name = forms.CharField(max_length=40, label="Full Name", required=True)
    card_number = forms.IntegerField(label="Card Number", required=True)
    cvc = forms.IntegerField(label="CVC", required=True)
    event_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    user_id = forms.CharField(max_length=100)
    event_price = forms.IntegerField()
    YEAR_CHOICES = (('17', '17'),('18', '18'),('19','19'),('20','20'),('21','21'),('22','22'))
    MONTH_CHOICES = (('01','01'),('02','02'),('03','03'),('04','04'),('05','05'),('06','06'),('07','07'),
                     ('08','08'),('09','09'),('10','10'),('11','11'),('12','12'))
    exp_month = forms.ChoiceField(choices=MONTH_CHOICES, label="Exp. Month", required=True)
    exp_year = forms.ChoiceField(choices=YEAR_CHOICES, label="Exp. Year", required=True)
    email = forms.CharField(max_length=40, label="Email", required=True)
    
    def __init__(self, *args, **kwargs):
        event_name = kwargs.pop('event_name')
        username = kwargs.pop('username')
        user_id = kwargs.pop('user_id')
        event_price = kwargs.pop('event_price')
        super(CreditCardForm, self).__init__(*args, **kwargs)
        self.fields['event_name'].initial = event_name
        self.fields['event_name'].widget = HiddenInput()
        self.fields['username'].initial = username
        self.fields['username'].widget = HiddenInput()
        self.fields['user_id'].initial = user_id
        self.fields['user_id'].widget = HiddenInput()
        self.fields['event_price'].widget = event_price
        self.fields['event_price'].widget = HiddenInput()
