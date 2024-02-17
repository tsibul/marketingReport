from django.db import models
import datetime
from marketing_report.models.settings_dictionary import SettingsDictionary


class FedRegion(SettingsDictionary):
    pass


class TypeGroup(SettingsDictionary):
    pass


class RegionToFedRegion(SettingsDictionary):
    fed_region = models.ForeignKey(FedRegion, on_delete=models.CASCADE)


class CustomerType(SettingsDictionary):
    group_discount = models.FloatField(default=0)
    code = models.CharField(max_length=2, default='')
    type_group = models.ForeignKey(TypeGroup, models.SET_NULL, null=True, blank=True, default=None)


class CustomerGroup(SettingsDictionary):
    customer_type = models.ForeignKey(CustomerType, models.SET_NULL, null=True)
    phone = models.CharField(max_length=255, default='')
    mail = models.CharField(max_length=255, default='')
    date_first = models.DateField(default=datetime.date(2000, 1, 1))
    date_last = models.DateField(default=datetime.date(2000, 1, 1))
    active = models.BooleanField(default=True)
    default = models.BooleanField(default=True)


class CustomerGroupFrigateId(models.Model):
    customer_group = models.ForeignKey(CustomerGroup, on_delete=models.CASCADE)
    frigate_code = models.CharField(max_length=30, unique=True)
