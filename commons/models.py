
'''
Created on 09-Jul-2019

@author: akshay.gupta
'''

from collections import defaultdict
from enum import Enum
import uuid

from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField

from django.apps import apps
from django.db import models
import pytz



STATUS_ENABLED = 1
STATUS_DISABLED = 0

class UserRole(Enum):
    CUSTOMER = 0
    CHEF = 4
    ORDER_MANAGER = 1
    SUPERVISOR = 2
    ADMIN = 3

class OrderStatus(Enum):
    CREATED = 0
    PENDING = 1
    OUT_FOR_DELIVERY = 2
    DELIVERED = 3
    CANCELLED = 4
    COMPLETED = 5    

STATUS_CHOICES = (
    (STATUS_ENABLED, 'Enable'),
    (STATUS_DISABLED, 'Disable'),
)


class OrderItemStatus(Enum):
    PENDING = 0
    COMPLETED = 1
    CANCELLED = 2
     
class OrderType(Enum):
    DINE_IN = 0
    TAKE_AWAY = 1
    HOME_DELIVERY = 2

class PaymentMode(Enum):
    CASH = 0
    ONLINE = 1
    PENDING = 2

        
TIMEZONE_CHOICES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class BulkCreateManager(object):
    """
    This helper class keeps track of ORM objects to be created for multiple
    model classes, and automatically creates those objects with `bulk_create`
    when the number of objects accumulated for a given model class exceeds
    `chunk_size`.
    Upon completion of the loop that's `add()`ing objects, the developer must
    call `done()` to ensure the final set of objects is created for all models.
    """

    def __init__(self, chunk_size=100):
        self._create_queues = defaultdict(list)
        self.chunk_size = chunk_size

    def _commit(self, model_class):
        model_key = model_class._meta.label
        model_class.objects.bulk_create(self._create_queues[model_key])
        """
        hack to get signal for bulk update event
        """
        # threading.Thread(target=event_handler.bulk_insert_event_handler, args=(model_key, self._create_queues[model_key],)).start()
        self._create_queues[model_key] = []

    def add(self, obj):
        """
        Add an object to the queue to be created, and call bulk_create if we
        have enough objs.
        """
        model_class = type(obj)
        model_key = model_class._meta.label
        self._create_queues[model_key].append(obj)
        if len(self._create_queues[model_key]) >= self.chunk_size:
            self._commit(model_class)

    def done(self):
        """
        Always call this upon completion to make sure the final partial chunk
        is saved.
        """
        for model_name, objs in self._create_queues.items():
            if len(objs) > 0:
                self._commit(apps.get_model(model_name))

class HangrooSetting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key_name = models.CharField(max_length=300)
    key_value =  models.CharField(max_length=300)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = AuditlogHistoryField()
    
    class Meta:
        db_table = 'hangroo_setting'
        ordering = ('-created_at', )

    def __str__(self):
        return str(self.key_name)
    

auditlog.register(HangrooSetting)
