from django.db import models
from commons.models import STATUS_CHOICES, STATUS_ENABLED
from autoslug.fields import AutoSlugField
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField
from user.models import Organisation
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=300)
    slug = AutoSlugField(populate_from='name')
    organisation = models.ForeignKey(Organisation, models.CASCADE, to_field='name')#, default='HangrooCafe-Banthra')
    status = models.IntegerField(default=STATUS_ENABLED, choices=STATUS_CHOICES)
    category = models.CharField(max_length=50)
    description = models.TextField()
    photo = models.ImageField(upload_to='product_photo',
                              blank=True)
    manufacturer = models.CharField(max_length=300,
                                    blank=True)
    price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = AuditlogHistoryField()
    class Meta:
        db_table = 'product'
        ordering = ('category','name', )
    def __str__(self):
        return str(self.category +" | "+  self.name+" :- ₹"+  str(self.price))



auditlog.register(Product)