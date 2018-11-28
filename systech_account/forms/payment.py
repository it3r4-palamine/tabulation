from django import forms
from ..models.payment import *

class Payment_type_form(forms.ModelForm):
	class Meta:
		model = PaymentType
		fields = ('name','company')

class Payment_form(forms.ModelForm):
	class Meta:
		model = Payment
		fields = ('enrollment',
				  'amount_paid',
				  'payment_date',
				  'official_receipt_no',
				  'company')