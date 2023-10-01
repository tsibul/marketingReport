from django.core.files.storage import FileSystemStorage
from django.db import models

fs = FileSystemStorage(location="/static/marketing/files")


class ImportCustomers (models.Model):
    frigat_id = models.IntegerField(db_index=True)
    form = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    inn = models.CharField(max_length=20, null=True)
    customer_type = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    all_phones = models.CharField(max_length=600, null=True, blank=True)
    mail = models.CharField(max_length=255, null=True, blank=True)
    all_mails = models.CharField(max_length=600, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    our_manager = models.CharField(max_length=255, blank=True)

