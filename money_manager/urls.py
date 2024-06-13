"""
URL configuration for money_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from finance import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('signup/', views.signup, name = 'signup'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('logout/', views.signout, name = 'logout'),
    path('signin/', views.signin, name = 'signin'),
    path('transaction/', views.transaction, name = 'transaction'),
    path('transaction/create/', views.create_transaction, name = 'create_transaction'),
    path('transaction/<int:id_transaction>/', views.transaction_details, name = 'transaction_details'),
    path('transaction/<int:id_transaction>/delete', views.delete_transaction, name = 'delete_transaction'),
    path('savings/', views.savings, name = 'savings'),
    path('savings/create/', views.create_saving, name = 'create_saving'),
    path('savings/delete/', views.delete_saving, name = 'delete_saving')
]
