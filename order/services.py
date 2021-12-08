from order.models import Order, OrderItem
from order.serializers import OrderSerializer, OrderItemSerializer
from commons.models import OrderStatus, HangrooSetting, OrderItemStatus,\
    OrderType
import datetime
from django.utils.timezone import make_aware


def get_pending_orders(profile):
    try:
        pending_orders = {}
        #TODO: add check for super admin or multi store manager
        ###get_created_orders
        created_orders = Order.objects.filter(status__in=[OrderStatus.CREATED], organisation=profile.organisation).order_by('created_at')
        if created_orders.exists():
            pending_orders["created_orders"] = OrderSerializer(created_orders, many=True).data
        ###get_accepted_orders
        accepted_orders = Order.objects.filter(status__in=[OrderStatus.PENDING],organisation=profile.organisation).order_by('created_at')
        if accepted_orders.exists():
            pending_orders["pending_orders"] = OrderSerializer(accepted_orders, many=True).data
            
    except Exception as e:
        print(e)
    return pending_orders

def get_pending_order_page_refresh_time():
    try:
        key_value = 10000   # 10 seconds default value
        key_data = HangrooSetting.objects.filter(key_name="ORDER_PAGE_REFRESH_TIME")
        if key_data.exists():
            key_data = key_data.first()
            key_value = int(key_data.key_value)*1000
    except Exception as e:
        print(e)
    return key_value

def get_pending_items(profile):
    try:
        pending_items = {}
        #TODO: add check for super admin or multi store manager
        ###get_table_items
        table_items = OrderItem.objects.filter(status__in=[OrderItemStatus.PENDING], order__order_type=OrderType.DINE_IN,  order__organisation=profile.organisation).order_by('created_at')
        if table_items.exists():
            pending_items["table_items"] = OrderItemSerializer(table_items, many=True).data
        ###get_packing_items
        packing_items = OrderItem.objects.filter(status__in=[OrderItemStatus.PENDING], order__order_type__in=[OrderType.HOME_DELIVERY, OrderType.TAKE_AWAY],  order__organisation=profile.organisation).order_by('created_at')
        if packing_items.exists():
            pending_items["packing_items"] = OrderItemSerializer(packing_items, many=True).data
            
    except Exception as e:
        print(e)
    return pending_items

def get_pending_item_page_refresh_time():
    try:
        key_value = 10000   # 10 seconds default value
        key_data = HangrooSetting.objects.filter(key_name="ITEM_PAGE_REFRESH_TIME")
        if key_data.exists():
            key_data = key_data.first()
            key_value = int(key_data.key_value)*1000
    except Exception as e:
        print(e)
    return key_value

def check_if_new_order_item(profile):
    created_time = datetime.datetime.now() - datetime.timedelta(minutes=1)
    #TODO: add check for super admin or multi store manager
    new_order_item = OrderItem.objects.filter(status__in=[OrderItemStatus.PENDING], created_at__gte=make_aware(created_time), order__organisation=profile.organisation).order_by('created_at')
    if new_order_item.exists():
        new_order_item = True
    else:
        new_order_item = False
    return new_order_item

def get_receipt_data(order_id):
    ###get_accepted_orders
    order = Order.objects.filter(id=order_id).get()
    order = OrderSerializer(order, many=False).data
    
    return order
        


