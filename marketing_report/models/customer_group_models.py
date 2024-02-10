from django.db import models
import datetime
from marketing_report.models.settings_dictionary import SettingsDictionary


class CustomerType(SettingsDictionary):
    group_discount = models.FloatField(default=0)
    code = models.CharField(max_length=2, default='')


class CustomerGroup(SettingsDictionary):
    customer_type = models.ForeignKey(CustomerType, models.SET_NULL, null=True)
    phone = models.CharField(max_length=255, default='')
    mail = models.CharField(max_length=255, default='')
    date_first = models.DateField(default=datetime.date(2000, 1, 1))
    date_last = models.DateField(default=datetime.date(2000, 1, 1))
    active = models.BooleanField(default=True)
    default = models.BooleanField(default=True)
