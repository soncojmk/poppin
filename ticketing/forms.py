from django import forms

class CreditCardForm(forms.Form):
    name = forms.CharField(max_length=40, label="Full Name", required=True)
    card_number = forms.IntegerField(label="Card Number", required=True)
    cvv = forms.IntegerField(label="cvv", required=True)
    
    YEAR_CHOICES = (('17', '17'),('18', '18'),('19','19'),('20','20'),('21','21'),('22','22'))
    MONTH_CHOICES = (('01','01'),('02','02'),('03','03'),('04','04'),('05','05'),('06','06'),('07','07'),
                     ('08','08'),('09','09'),('10','10'),('11','11'),('12','12'))
    exp_month = forms.ChoiceField(choices=MONTH_CHOICES, label="Exp. Month", required=True)
    exp_year = forms.ChoiceField(choices=YEAR_CHOICES, label="Exp. Year", required=True)
