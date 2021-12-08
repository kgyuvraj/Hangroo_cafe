from django.contrib import admin
from django.db import models
from order.models import OrderItem, Order
from commons.models import OrderItemStatus
from django.forms.widgets import Textarea
# Register your models here.


class OrderItemInline(admin.TabularInline):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 40})},
    }
    model = OrderItem
    extra = 0   
    can_delete = False
    list_display = ('product.name',)
    search_fields = ('product.name',)
    exclude = ("created_by", "updated_by",)


def update_amount_settlement(instance):
    #### get order items
    pending_amount = 0
    order_items = OrderItem.objects.filter(order = instance)
    if order_items.exists():
        for order_item in order_items:
            if not order_item.status == OrderItemStatus.CANCELLED:
                pending_amount = pending_amount + (order_item.product.price * order_item.qty)
    #### get order_instance
    cash_amount = instance.amount_paid_cash
    online_amount = instance.amount_paid_online
    discount_amount = instance.discount_amount
    instance.amount_pending  = pending_amount -(cash_amount+online_amount+discount_amount)
    instance.save()


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 40})},
    }
    inlines = [OrderItemInline]
    readonly_fields = ("amount_pending","created_at", "updated_at", "created_by", "updated_by")
    list_display = ("__str__","status","order_type","created_at", "created_by", "updated_by",)
    list_filter = ("organisation","status","order_type","created_at","amount_pending","discount_amount",)
    #search_fields = ('stock__name', 'stock__symbol')
    exclude = ("payment_mode",)
    def save_formset(self, request, form, formset, change): 
        if formset.model == OrderItem:
            instances = formset.save(commit=False)
            for instance in instances:
                try:
                    if not instance.created_by:
                        pass
                except Exception as e:
                    instance.created_by = request.user
                instance.updated_by = request.user
                instance.save()
            if len(instances) >0:
                update_amount_settlement(instances[0].order)
        else:
            formset.save()
    
    def save_model(self, request, obj, form, change): 
        try:
            if not obj.created_by:
                pass
        except Exception as e:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()
        update_amount_settlement(obj)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_display = ("__str__","status","created_at", "created_by", "updated_by",)
    list_filter = ("status","created_at")
    def save_model(self, request, obj, form, change): 
        try:
            if not obj.created_by:
                pass
        except Exception as e:
            print(e)
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()