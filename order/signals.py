'''
Created on 11-Mar-2021

@author: akshay.gupta
'''
from django.db.models.signals import post_save, pre_init, post_init, pre_save, \
    pre_delete, post_delete
from django.dispatch.dispatcher import receiver

from order.models import OrderItem
from commons.models import OrderItemStatus
from inventory.models import Inventory


@receiver([post_save], sender=OrderItem)
def update_inventory(sender, instance, **kwargs):
    print("Started Signal")
    ### check if order is completed
    if instance.status == OrderItemStatus.COMPLETED:
        ### check if product has some inventory
        product = instance.product
        query_set = Inventory.objects.filter(name=product)
        if query_set.exists():
            ### reduce the inventory quantity
            inventory = query_set.get()
            inventory.qty = inventory.qty - instance.qty
            inventory.save()
    print("End Signal")
    
