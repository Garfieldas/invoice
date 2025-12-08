from django.contrib import admin
from customers.models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "company_name")
    search_fields = ('first_name', 'last_name', 'company_name', 'address', 'company_code')
