from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError
from .forms import create_transaction_form
from .models import Transaction

# Inicio
def home(request):
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

	incomes = expenses = 0
	for trans in transactions:
		if trans.category == 'INGRESO':
			incomes += trans.value
		else:
			expenses += trans.value  

	total = incomes - expenses

	return render(request, 'dashboard.html', {'total': total, 'incomes': incomes, 'expenses': expenses})

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
