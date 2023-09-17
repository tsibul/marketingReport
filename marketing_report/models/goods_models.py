from django.db import models
import datetime

from marketing_report.models.goods_types_models import GoodCrmType, GoodMatrixType
from marketing_report.models.color_models import ColorScheme


class Goods(models.Model):
    """details of item detail# if exist
        name - name of goods
        item_name - item code
        detail_name - name of detail
        detail_place - if prinring possible"""
    name = models.CharField(max_length=200, null=True, blank=True)
    item_name = models.CharField(max_length=20, null=True, blank=True)
    eco = models.BooleanField(default=True)
    matrix = models.ForeignKey(GoodMatrixType, models.SET_NULL, null=True, default=None)
    crm = models.ForeignKey(GoodCrmType,  models.SET_NULL, null=True, default=None)
    color_scheme = models.ForeignKey(ColorScheme, models.SET_NULL, null=True)
    multicolor = models.BooleanField(default=False)
    date_first = models.DateField(default=datetime.date(2000, 1, 1))
    date_last = models.DateField(default=datetime.date(2000, 1, 1))

    def __repr__(self):
        return self.name

    def __str__(self):
        return str(self.name)
