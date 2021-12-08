import uuid


from django.contrib.auth.models import User
from django.db import models
from enumfields import EnumIntegerField

from commons.models import OrderStatus, OrderItemStatus, PaymentMode, OrderType
from product.models import Product
from auditlog.registry import auditlog
from user.models import Organisation


# Create your models here.
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, models.CASCADE, to_field='name')#, default='HangrooCafe-Banthra')
    status = EnumIntegerField(default=OrderStatus.CREATED, enum=OrderStatus)
    order_type = EnumIntegerField(default=OrderType.HOME_DELIVERY, enum=OrderType)
    payment_mode =  EnumIntegerField(default=PaymentMode.CASH, enum=PaymentMode)
    remark = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name='order_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name='order_updated_by')
    amount_paid_online = models.IntegerField(default=0)
    amount_paid_cash = models.IntegerField(default=0)
    amount_pending = models.IntegerField(default=0)
    discount_amount = models.IntegerField(default=0)


    class Meta:
        db_table = 'order'
        ordering = ('-created_at', )

    def __str__(self):
        return str(self.customer.get_full_name()) + "-" + str(self.id.hex)


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='order_items')
    status = EnumIntegerField(default=OrderItemStatus.PENDING, enum=OrderItemStatus)
    qty = models.IntegerField(default=1)
    remark = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='order_item_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='order_item_updated_by')


    class Meta:
        #abstract = True
        db_table = 'order_item'

    def __str__(self):
        return str(self.product)

auditlog.register(Order)
auditlog.register(OrderItem)