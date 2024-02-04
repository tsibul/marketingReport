import datetime
from django.db import models
from django.core.files.storage import FileSystemStorage
from marketing_report.models import SettingsDictionary

fs_patterns = FileSystemStorage(location='files/patterns')


class ColorScheme(SettingsDictionary):
    """ color scheme IV, Grant, Eco """


class Color(SettingsDictionary):
    """ id - (07)
        name - name
        pantone - pantone color
        code - HEX"""
    code = models.CharField(max_length=10)
    pantone = models.CharField(max_length=20, default='')
    hex = models.CharField(max_length=7)
    color_scheme = models.ForeignKey(ColorScheme, models.SET_NULL, null=True)
    date_first = models.DateField(default=datetime.date(2000, 1, 1))
    date_last = models.DateField(default=datetime.date(2000, 1, 1))
    standard = models.BooleanField(default=True)

    def __repr__(self):
        return str(self.code + ', ' + self.color_scheme.name)

    def __str__(self):
        return str(self.code + ', ' + self.color_scheme.name)

    @staticmethod
    def order_default():
        return ['color_scheme', 'code']


class PrintType(SettingsDictionary):
    """ Pad, screen, UW, soft_touch etc."""

