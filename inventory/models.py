from django.db import models
from product.models import Product
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField
# Create your models here.
class Inventory(models.Model):
    name = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    qty = models.DecimalField(max_digits=6,
                                           decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = AuditlogHistoryField()
    class Meta:
        db_table = 'inventory'

    def __str__(self):
        return str(self.name)


auditlog.register(Inventory)