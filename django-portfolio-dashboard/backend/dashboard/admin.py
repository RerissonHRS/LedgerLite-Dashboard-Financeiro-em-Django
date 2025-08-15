from django.contrib import admin
from .models import Sale

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('date', 'product', 'category', 'unit_price', 'quantity', 'total')
    list_filter = ('category', 'date')
    search_fields = ('product', 'category')
