from django.contrib import admin
from product.models import Product

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('name','category', 'price','organisation','description', )
    list_filter = ('status', 'category','organisation')
    search_fields = ('name',)