from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.db import IntegrityError

# Create your views here.

def home(request):
	return render(request, "home.html")

def signup(request):
	if request.method == 'GET':
		return render(request, "signup.html", {'form': UserCreationForm})
	else:
		if request.POST['password1'] == request.POST['password2']:
			try:			
				user = User.objects.create_user(username = request.POST['username'],
					password = request.POST['password1'])
				user.save()
				login(request, user)
				return redirect('dashboard')
			except IntegrityError:
				return render(request, "signup.html", {
					'form': UserCreationForm,
					'error': "Usuario existente."
				})

		return render(request, "signup.html", {
				'form': UserCreationForm,
				'error': "Las contraseñas no coinciden."
			})

def dashboard(request):
	return render(request, 'dashboard.html')

def signout(request):
	logout(request)
	return redirect('home')