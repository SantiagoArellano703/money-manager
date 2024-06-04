from django.forms import ModelForm
from .models import Transaction

class create_transaction(ModelForm):
	class Meta:
		model = Transaction
		fields = ['category', 'value', 'description']