from django.db import models
import datetime

from marketing_report.models.goods_types_models import CrmType, MatrixType
from marketing_report.models.color_models import ColorScheme
from marketing_report.models.settings_dictionary import SettingsDictionary


class Goods(SettingsDictionary):
    """details of item detail# if exist
        name - name of goods
        item_code - item code
        detail_name - name of detail
        detail_place - if prinring possible"""
    item_code = models.CharField(max_length=20, null=True, blank=True)
    eco = models.BooleanField(default=True)
    matrix_type = models.ForeignKey(MatrixType, models.SET_NULL, null=True, default=None)
    crm_type = models.ForeignKey(CrmType,  models.SET_NULL, null=True, default=None)
    color_scheme = models.ForeignKey(ColorScheme, models.SET_NULL, null=True)
    multicolor = models.BooleanField(default=False)
    date_first = models.DateField(default=datetime.date(2000, 1, 1))
    date_last = models.DateField(default=datetime.date(2000, 1, 1))

    def __repr__(self):
        return self.item_code

    def __str__(self):
        return str(self.item_code)

    @staticmethod
    def order_default():
        return ['item_code']
