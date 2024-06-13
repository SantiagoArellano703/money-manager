from django.contrib import admin
from .models import Transaction, Saving

class trans_admin(admin.ModelAdmin):
	readonly_fields = ("date",)

# Register your models here.
admin.site.register(Transaction, trans_admin)
admin.site.register(Saving)