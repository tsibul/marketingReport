from django.db import models

from marketing_report.models.goods_types_models import GoodCrmType, GoodMatrixType
from marketing_report.models.color_models import ColorScheme, PrintGroup


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
    print_group = models.ForeignKey(PrintGroup, models.SET_NULL, null=True, blank=True)
    detail1_name = models.CharField(max_length=60)
    detail1_place = models.BooleanField(default=False)
    detail2_name = models.CharField(max_length=60, default='', null=True, blank=True)
    detail2_place = models.BooleanField(default=False)
    detail3_name = models.CharField(max_length=60, default='', null=True, blank=True)
    detail3_place = models.BooleanField(default=False)
    detail4_name = models.CharField(max_length=60, default='', null=True, blank=True)
    detail4_place = models.BooleanField(default=False)
    detail5_name = models.CharField(max_length=60, default='', null=True, blank=True)
    detail5_place = models.BooleanField(default=False)
    detail6_name = models.CharField(max_length=60, default='', null=True, blank=True)
    detail6_place = models.BooleanField(default=False)

    def __repr__(self):
        return self.name

    def __str__(self):
        return str(self.name)
