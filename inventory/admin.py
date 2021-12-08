from django.contrib import admin
from inventory.models import Inventory

# Register your models here.

@admin.register(Inventory)
class OrderItemAdmin(admin.ModelAdmin):
    model = Inventory
    list_display = ("__str__","qty","updated_at", )