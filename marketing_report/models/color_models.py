from django.db import models
from django.core.files.storage import FileSystemStorage

fs_patterns = FileSystemStorage(location='files/patterns')


class ColorScheme(models.Model):
    """ color scheme IV, Grant, Eco """
    scheme_name = models.CharField(max_length=13)

    def __repr__(self):
        return self.scheme_name

    def __str__(self):
        return str(self.scheme_name)


class Color(models.Model):
    """ id - (07)
        name - name
        pantone - pantone color
        code - HEX"""
    color_id = models.CharField(max_length=10)
    pantone = models.CharField(max_length=20, default='')
    color_name = models.CharField(max_length=60)
    color_code = models.CharField(max_length=7)
    color_scheme = models.ForeignKey(ColorScheme, models.SET_NULL, null=True)

    def __repr__(self):
        return str(self.color_id + ', ' + self.color_scheme.scheme_name)

    def __str__(self):
        return str(self.color_id + ', ' + self.color_scheme.scheme_name)


class PrintType(models.Model):
    """ Pad, screen, UW, soft_touch etc."""
    type_name = models.CharField(max_length=20)

    def __repr__(self):
        return self.type_name

    def __str__(self):
        return str(self.type_name)

