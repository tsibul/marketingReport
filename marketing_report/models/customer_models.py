from django.db import models
import datetime
from marketing_report.models import CustomerType, CustomerGroup, FedRegion


class Customer(models.Model):
    """type - agency, dealer, etc.
        number of Region"""
    form = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    inn = models.CharField(max_length=20, null=True)
    region = models.CharField(max_length=2)
    customer_group = models.ForeignKey(CustomerGroup, models.SET_NULL, null=True, default=None)
    customer_type = models.ForeignKey(CustomerType, models.SET_NULL, null=True, default=None)
    frigate_code = models.CharField(max_length=30, default='', db_index=True, unique=True)
    phone = models.CharField(max_length=255, blank=True)
    all_phones = models.CharField(max_length=600, null=True, blank=True)
    mail = models.CharField(max_length=255, null=True, blank=True)
    all_mails = models.CharField(max_length=600, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    our_manager = models.CharField(max_length=255, blank=True)
    date_import = models.DateField(default=datetime.date(2000, 1, 1))
    date_first = models.DateField(default=datetime.date(2000, 1, 1))
    date_last = models.DateField(default=datetime.date(2000, 1, 1))
    active = models.BooleanField(default=True)
    internal = models.BooleanField(default=False)
    new = models.BooleanField(default=False)
    fed_region = models.ForeignKey(FedRegion, models.SET_NULL, null=True, default=None)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        ordering = ['name']

    @staticmethod
    def order_default():
        return ['name']

    # def save(self, *args, **kwargs):
        # if self.group:
        #     self.name = self.group.name
        # else:
        #     self.name = self.customer.name
        # super().save(*args, **kwargs)

    def default_group(self):
        default_group = CustomerGroup(
            customer_type=self.customer_type,
            name=self.name,
            phone=self.phone,
            mail=self.mail,
            date_first=self.date_first,
            date_last=self.date_last,
            active=self.active,
            default=True,
            deleted=False
        )
        default_group.save()
        self.customer_group = default_group
        # return default_group

