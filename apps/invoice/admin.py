from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from invoice.models import Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'customer', 'invoice_number', 'total_price', 'created_at')
    search_fields = ('user', 'customer', 'invoice_number', 'created_at')
    inlines = [InvoiceItemInline]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs = super().get_queryset(request)
        return qs.select_related('user', 'customer')
    
@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'name', 'amount', 'price')
    search_fields = ('user', 'customer', 'invoice_number', 'created_at')

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs = super().get_queryset(request)
        return qs.select_related('invoice', 'invoice__user')