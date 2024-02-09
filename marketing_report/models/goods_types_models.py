from django.db import models
from marketing_report.models.settings_dictionary import SettingsDictionary


class BusinessUnit(SettingsDictionary):
    """
    Sales Unit is a
    """
    code = models.IntegerField(default=0)


class MatrixType(SettingsDictionary):
    """
    GoodMatrixType is a
    """


class CrmType(SettingsDictionary):
    """
    GoodCrmType is a
    """
    business_unit = models.ForeignKey(BusinessUnit, models.SET_NULL, null=True, blank=True)
