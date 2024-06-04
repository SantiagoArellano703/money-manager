from django.contrib import admin
from .models import Transaction

class trans_admin(admin.ModelAdmin):
	readonly_fields = ("date",)

# Register your models here.
admin.site.register(Transaction, trans_admin)