import datetime

from django.core.files.storage import FileSystemStorage
from django.db import models

fs = FileSystemStorage(location="/static/marketing_report/files")


class ImportCustomers (models.Model):
    """
    Model for Customer Import
    """
    import_date = models.DateField(default=datetime.date(2024, 1, 31))
    frigate_code = models.CharField(max_length=30, unique=True)
    form = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    inn = models.CharField(max_length=20, null=True)
    region = models.CharField(max_length=2, default='', blank=True, null=True)
    customer_type = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    all_phones = models.CharField(max_length=600, null=True, blank=True)
    mail = models.CharField(max_length=255, null=True, blank=True)
    all_mails = models.CharField(max_length=600, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    our_manager = models.CharField(max_length=255, blank=True)
    changed = models.BooleanField(default=False)
    new = models.BooleanField(default=False)
    internal = models.BooleanField(default=False)

