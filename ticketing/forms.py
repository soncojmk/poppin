from django import forms

class CreditCardForm(forms.Form):
    cvv = forms.IntegerField()
    card_number = forms.IntegerField()
    name = forms.CharField(max_length=40)
    exp_year = forms.Integer()
    exp_month = forms.Integer()
