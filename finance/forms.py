from django.forms import ModelForm
from .models import Transaction, Saving

class create_transaction_form(ModelForm):
	class Meta:
		model = Transaction
		fields = ['category', 'value', 'description', 'payment_method']

class create_saving_form(ModelForm):
	class Meta:
		model = Saving
		fields = ['goal', 'percentage']