from decimal import Decimal, ROUND_HALF_UP
from finance.models import Transaction, Saving
from django.contrib.auth.models import User

def get_data(request):
	transactions = Transaction.objects.filter(user = request.user)

	incomes = expenses = 0
	for trans in transactions:
		if trans.category == 'INGRESO':
			incomes += trans.value
		else:
			expenses += trans.value  

	total = incomes - expenses

	try:
		saving = Saving.objects.get(user=request.user)
	except Saving.DoesNotExist:
		saving = None

	saving_current = 0
	if saving != None:
		transactions = Transaction.objects.filter(user = request.user, category='INGRESO', date__gt=saving.date)
		percentage = saving.percentage * Decimal('0.01')

		for trans in transactions:
			if saving_current < saving.goal:
				saving_current += trans.value * percentage

				if saving_current > saving.goal:
					saving_current = saving.goal

		if saving_current != 0:
			saving_current = saving_current.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
		saving.current_value = saving_current
		saving.save()
	
	avaible = total - saving_current

	return (total, avaible, incomes, expenses, saving_current)
	