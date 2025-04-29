from django.contrib import admin
from .models import Stock, Order, User
from django.contrib.auth.admin import UserAdmin

class StockAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'current_price']
    search_fields = ['id', 'name']
    list_editable = ['current_price']
    ordering = ['id']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'stock', 'order_type', 'quantity', 'price', 'timestamp']
    list_filter = ['order_type', 'timestamp']
    raw_id_fields = ['user', 'stock']

admin.site.register(Stock, StockAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(User, UserAdmin)