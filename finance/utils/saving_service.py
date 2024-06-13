from decimal import Decimal
from finance.models import Transaction, Saving
from django.contrib.auth.models import User

def make_saving(income, income_new, request):
	try:
		saving = Saving.objects.get(user=request.user)

		if saving.current_value < saving.goal:
			percentage = saving.percentage * Decimal('0.01')

			saving_current = income * percentage
			saving_new = (income_new * percentage) - saving_current

			saving.current_value += saving_new

			if saving.current_value > saving.goal:
				saving.current_value = saving.goal

			saving.save()
		return
	except:
		return None

def update_saving(income, request):
	try:
		if saving.current_value < saving.goal:
			saving = Saving.objects.get(user=request.user)
			percentage = saving.percentage * Decimal('0.01')
			saving_current = income * percentage
			saving.current_value -= saving_current

			if saving.current_value > saving.goal:
				saving.current_value = saving.goal
				
			saving.save()
		return
	except:
		return None
	