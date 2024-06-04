from django.forms import ModelForm
from .models import Transaction

class create_transaction_form(ModelForm):
	class Meta:
		model = Transaction
		fields = ['category', 'value', 'description']