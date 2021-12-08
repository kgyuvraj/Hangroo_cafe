from rest_framework import serializers
from order.models import Order, OrderItem
from commons import fields
import commons
from product.serializers import ProductSerializer
from user.serializers import UserSerializer
from rest_framework.fields import SerializerMethodField
import datetime
from datetime import timezone, timedelta
from commons.models import OrderItemStatus


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    status = fields.EnumField(enum=commons.models.OrderItemStatus)
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    status = fields.EnumField(enum=commons.models.OrderStatus)
    order_type = fields.EnumField(enum=commons.models.OrderType)
    payment_mode = fields.EnumField(enum=commons.models.PaymentMode)
    order_items = OrderItemSerializer(many=True, read_only=True)
    customer = UserSerializer(many=False, read_only=True)    
    created_at = serializers.DateTimeField(format='%I:%M %p')
    wait_time = SerializerMethodField("get_wait_time_serializer")
    order_amount = SerializerMethodField("get_order_amount_serializer")
    class Meta:
        model = Order
        #fields = ("id","status","order_type","payment_mode", "order_items",)
        fields = "__all__"

        
    def get_wait_time_serializer(self, obj):
        timedelta
        #request = self.context.get('request')
        delta = datetime.datetime.now(timezone.utc) - obj.created_at
        return  int(delta.seconds/60)
    def get_order_amount_serializer(self, obj):
        ####get order Items from the db
        order_items = OrderItem.objects.filter(order=obj)
        sub_total = 0
        if order_items.exists():
            for item in order_items:
                if not item.status == OrderItemStatus.CANCELLED:
                    sub_total = sub_total + item.qty*item.product.price
        return sub_total