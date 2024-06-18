from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError
from .forms import create_transaction_form, create_saving_form
from .models import Transaction, Saving
from decimal import Decimal
from .utils.services import *

# Inicio
def home(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	return render(request, "home.html")

# Registro y login
def signup(request):
	if request.method == 'GET':
		return render(request, "signup.html")
	else:
		if request.POST['password1'] == request.POST['password2']:
			try:			
				user = User.objects.create_user(username = request.POST['username'],
					password = request.POST['password1'])
				user.save()
				login(request, user)
				return redirect('dashboard')
			except IntegrityError:
				return render(request, "signup.html", {'error': "Usuario existente."})

		return render(request, "signup.html", {'error': "Las contraseñas no coinciden."})

def signout(request):
	logout(request)
	return redirect('home')

def signin(request):
	if request.method == 'GET':
		return render(request, "signin.html")
	else:
		user = authenticate(request, username = request.POST['username'], password = request.POST['password'])

		if user is None:
			return render(request, "signin.html", {'error': 'Usuario o contraseña incorrecta.'})

		login(request, user)
		return redirect('dashboard')

# Transacciones
@login_required
def dashboard(request):
	transactions = Transaction.objects.filter(user = request.user)

	(total, avaible, incomes, expenses, saving_current, graphic_values) = get_data(request)

	return render(request, 'dashboard.html', {
		'total': total, 'incomes': incomes, 'expenses': expenses,
		'avaible': avaible, 'saving_current': saving_current, 'graphic_values': graphic_values})

@login_required
def transaction(request):
	category = request.GET.getlist('filter')

	if not category:
		category = ['AMBOS']

	if not 'AMBOS' in category:
		transactions = Transaction.objects.filter(user = request.user, category=category[0]).order_by('-date')
	else:
		transactions = Transaction.objects.filter(user = request.user).order_by('-date')

	return render(request, "transaction.html", {'transactions': transactions, 'category': category})

@login_required
def create_transaction(request):
	if request.method == 'GET':
		return render(request, "create_transaction.html")
	else:
		try:
			(total, avaible, incomes, expenses, saving_current) = get_data(request)

			if request.POST['category'] == 'GASTO' and int(request.POST['value']) > int(avaible):
				return render(request, "create_transaction.html", {'error': 'El saldo disponible es insuficiente.'})

			form = create_transaction_form(request.POST)
			new_transaction = form.save(commit=False)
			new_transaction.user = request.user
			new_transaction.save()
			return redirect('transaction')
		except ValueError:
			return render(request, "create_transaction.html", {'error': 'Por favor ingresa datos válidos'})

@login_required
def transaction_details(request, id_transaction):
	trans = get_object_or_404(Transaction, pk=id_transaction, user=request.user)
	income = trans.value if 'INGRESO' in trans.category else Decimal('0.00')

	if request.method == 'GET':
		return render(request, 'transaction_details.html', {'transaction': trans})
	else:
		try:
			form = create_transaction_form(request.POST, instance=trans)
			form.save()
			return redirect('transaction')
		except ValueError:
			return render(request, "transaction_details.html", {'error': 'Por favor ingresa datos válidos'})

@login_required
def delete_transaction(request, id_transaction):
	trans = get_object_or_404(Transaction, pk=id_transaction, user=request.user)

	if request.method == 'POST':
		trans.delete()
	return redirect('transaction')

# Ahorros

@login_required
def savings(request):

	try:
		get_data(request)
		saving = Saving.objects.get(user=request.user)
	except Saving.DoesNotExist:
		saving = None

	return render(request, 'savings.html', {'saving': saving})

@login_required
def create_saving(request):
	try:
		saving = Saving.objects.get(user=request.user)
	except Saving.DoesNotExist:
		saving = None


	if request.method == 'GET':
		return render(request, "create_saving.html", {'saving': saving})
	else:
		try:
			if saving == None:
				form = create_saving_form(request.POST)
				new_saving = form.save(commit=False)
				new_saving.user = request.user
				new_saving.save()
			else:
				form = create_saving_form(request.POST, instance=saving)
				form.save()

			return redirect('savings')
		except ValueError:
			return render(request, "create_saving.html", {'saving': saving, 'error': 'Por favor ingresa datos válidos'})

@login_required
def delete_saving(request, used):
	saving = get_object_or_404(Saving, user=request.user)

	if request.method == 'POST':
		if used == 1:
			transaction = Transaction(category='GASTO', value=saving.goal,
				description="Uso de ahorros", user=request.user)
			transaction.save()

		saving.delete()
	return redirect('savings')